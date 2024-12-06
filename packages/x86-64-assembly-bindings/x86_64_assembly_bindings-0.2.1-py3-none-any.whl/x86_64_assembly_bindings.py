from __future__ import annotations
from enum import Enum, EnumMeta
from typing import Literal
import os

class Program:
    CURRENT = None
    def __init__(self, name:str|None = None):
        self.name = name
        self.lines:list[Instruction|Memory|str] = []
        Program.CURRENT = self

    def append(self, component:Instruction|Memory):
        self.lines.append(component)

    def write(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "\n".join(
                    i
                if isinstance(i, str) else
                    f"{'    ' if isinstance(i, Instruction) else ''}{i.write()}"
            for i in self.lines
        )

    def save(self, path:str):
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(self.write())

    def comment(self, text:str):
        self.append(f"; {text}")

    def append_line(self, line:str):
        self.append(line)

    def new_line(self):
        self.append("")

    def exit_program(self):
        self.append("    mov rax, 60")
        self.append("    mov rdi, 0")
        self.append("    syscall")

    def compile(self, program:str|None = None, save:bool = True, **arguments_:dict[str, any]):
        program = self.name if program is None else program

        if program is None:
            raise RuntimeError("You must specify a program name either in the \"program\" argument of the \"compile\" function, by setting the \"name\" attribute of your \"Program\" instance or by specifying it as the \"name\" argument when creating your \"Program\" instance.")

        if save:self.save(f"{program}.asm")
        args = {
            "-f":"elf64",
            "-o":f"\"{program}.o\""
        }
        args.update({f"-{k}":str(v) for k,v in arguments_.items()})
        command = ("yasm "+
            ' '.join([f"{k} {v}" for k,v in args.items()])+
            f" \"{program}.asm\"")

        os.system(command)

    def link(self, output:str|None = None, programs:set[Program|str]|None = None, args:dict[str, any]|None = None, lib_paths:set[str]|None = None, libs:set[str]|None = None, script:str|None = None):
        output = self.name if output is None else output
        
        programs = set() if programs is None else programs
        if self.name is not None:
            programs.add(self.name)

        if not programs:
            raise RuntimeError("The \"programs\" argument cannot be empty unless the \"Program\" instance's \"name\" attribute is set.")

        if output is None:
            raise RuntimeError("You must specify a program name either by passing it as the \"output\" argument when calling the link function, by setting the \"name\" attribute of your \"Program\" instance or by specifying it as the \"name\" argument when creating your \"Program\" instance.")

        out_file = f"-o \"{output}\""
        o_files = "\"" + ' \"'.join([f"{f}.o\"" for f in programs])
        script = "" if script is None else f"-T \"{script}\""
        lib_paths = "" if lib_paths is None else "\"-L"+' \"-L'.join(
            [f"{p}\"" for p in lib_paths]
        )
        libs = "" if libs is None else "\"-l"+' \"-l'.join(
            [f"{l}\"" for l in libs]
        )
        args:str = "" if args is None else ' '.join([f"-{k}" + ("" if v is None else f" \"{v}\"") for k,v in args.items()])


        command = f"ld {out_file} {script} {o_files} {lib_paths} {libs} {args}"

        os.system(command)


    def run(self, *args:list[any], compile_args:dict|None = None, link_args:dict|None = None, skip_compile:bool = False, skip_link:bool = False):
        if self.name is None:
            raise RuntimeError("The \"name\" attribute of the \"Program\" instance must be specified to run the program.")

        compile_args = {} if compile_args is None else compile_args
        link_args = {} if link_args is None else link_args

        if not skip_compile:
            self.compile(**compile_args)
        if not skip_link:
            self.link(**link_args)
        
        args:str = ' '.join([f"'{a}'" for a in args])

        os.system(f"./{self.name} {args}")


Program()# create the current program


class Block:
    block_counter = 0

    def __init__(self, label:str|None = None):
        self.label = label if label else f"block{Block.block_counter}"
        if label is None:
            Block.block_counter += 1

    def __str__(self):
        return f"{self.label}"

    def write(self):
        return f"{self}:"

    def __call__(self, recorder:Program|None = None):
        (recorder if recorder else Program.CURRENT).append(self)
        return self


class MemorySize(Enum):
    BYTE = 8
    WORD = 16
    DWORD = 32
    QWORD = 64
    
    def __eq__(self, other:MemorySize):
        if not isinstance(other, MemorySize):
            return False
        return self.value == other.value

    def __gt__(self, other:Register):
        if not isinstance(other, MemorySize):
            return False
        return self.value > other.value

    def __lt__(self, other:Register):
        if not isinstance(other, MemorySize):
            return False
        return self.value < other.value

    def __repr__(self):
        return f"{self.name}({self.value})"

    def __str__(self):
        return repr(self)

    @property
    def grow(self):
        match self:
            case self.BYTE:
                return self.WORD
            case self.WORD:
                return self.DWORD
            case self.DWORD:
                return self.QWORD
            case self.QWORD:
                return None

    @property
    def shrink(self):
        match self:
            case self.BYTE:
                return None
            case self.WORD:
                return self.BYTE
            case self.DWORD:
                return self.WORD
            case self.QWORD:
                return self.DWORD


    @property
    def sec_data_write(self):
        match self:
            case self.BYTE:
                return "db"
            case self.WORD:
                return "dw"
            case self.DWORD:
                return "dd"
            case self.QWORD:
                return "dq"

    @property
    def sec_bss_write(self):
        match self:
            case self.BYTE:
                return "resb"
            case self.WORD:
                return "resw"
            case self.DWORD:
                return "resd"
            case self.QWORD:
                return "resq"

RegisterDataType = tuple[str, MemorySize, Literal[0]|Literal[1]]
#                       [name, size, position (0 = upper bytes, 1 = lower bytes)]

class RegisterData(Enum):
    """
    This enum defines all the sizes and other shared properties of all registers.
    """
    # main registers
    ah:RegisterDataType = ("ah", MemorySize.BYTE, 0)
    al:RegisterDataType = ("al", MemorySize.BYTE, 1)
    dx:RegisterDataType = ("dx", MemorySize.WORD, 0)
    ax:RegisterDataType = ("ax", MemorySize.WORD, 1)
    edx:RegisterDataType = ("edx", MemorySize.DWORD, 0)
    eax:RegisterDataType = ("eax", MemorySize.DWORD, 1)
    rdx:RegisterDataType = ("rdx", MemorySize.QWORD, 0)
    rax:RegisterDataType = ("rax", MemorySize.QWORD, 1)

    rcx:RegisterDataType = ("rcx", MemorySize.QWORD, 0)
    ecx:RegisterDataType = ("ecx", MemorySize.DWORD, 0)
    cx:RegisterDataType = ("cx", MemorySize.WORD, 0)
    ch:RegisterDataType = ("ch", MemorySize.BYTE, 0)
    cl:RegisterDataType = ("cl", MemorySize.BYTE, 1)
    
    dh:RegisterDataType = ("dh", MemorySize.BYTE, 0)
    dl:RegisterDataType = ("dl", MemorySize.BYTE, 1)

    rbx:RegisterDataType = ("rbx", MemorySize.QWORD, 0)
    ebx:RegisterDataType = ("ebx", MemorySize.DWORD, 0)
    bx:RegisterDataType = ("bx", MemorySize.WORD, 0)
    bh:RegisterDataType = ("bh", MemorySize.BYTE, 0)
    bl:RegisterDataType = ("bl", MemorySize.BYTE, 1)

    rsp:RegisterDataType = ("rsp", MemorySize.QWORD, 0)
    esp:RegisterDataType = ("esp", MemorySize.DWORD, 0)
    sp:RegisterDataType = ("sp", MemorySize.WORD, 0)
    spl:RegisterDataType = ("spl", MemorySize.BYTE, 1)

    rbp:RegisterDataType = ("rbp", MemorySize.QWORD, 0)
    ebp:RegisterDataType = ("ebp", MemorySize.DWORD, 0)
    bp:RegisterDataType = ("bp", MemorySize.WORD, 0)
    bpl:RegisterDataType = ("bpl", MemorySize.BYTE, 1)



    # other 64
    rdi:RegisterDataType = ("rdi", MemorySize.QWORD, 0)
    rsi:RegisterDataType = ("rsi", MemorySize.QWORD, 0)
    r8:RegisterDataType = ("r8", MemorySize.QWORD, 0)
    r9:RegisterDataType = ("r9", MemorySize.QWORD, 0)
    r10:RegisterDataType = ("r10", MemorySize.QWORD, 0)
    r11:RegisterDataType = ("r11", MemorySize.QWORD, 0)

    # other 32
    esi:RegisterDataType = ("esi", MemorySize.DWORD, 0)
    edi:RegisterDataType = ("edi", MemorySize.DWORD, 0)
    r8d:RegisterDataType = ("r8d", MemorySize.DWORD, 0)
    r9d:RegisterDataType = ("r9d", MemorySize.DWORD, 0)
    r10d:RegisterDataType = ("r10d", MemorySize.DWORD, 0)
    r11d:RegisterDataType = ("r11d", MemorySize.DWORD, 0)

    # other 16
    si:RegisterDataType = ("si", MemorySize.WORD, 0)
    di:RegisterDataType = ("di", MemorySize.WORD, 0)
    r8w:RegisterDataType = ("r8w", MemorySize.WORD, 0)
    r9w:RegisterDataType = ("r9w", MemorySize.WORD, 0)
    r10w:RegisterDataType = ("r10w", MemorySize.WORD, 0)
    r11w:RegisterDataType = ("r11w", MemorySize.WORD, 0)

    # other 8
    sil:RegisterDataType = ("sil", MemorySize.BYTE, 1)
    dil:RegisterDataType = ("dil", MemorySize.BYTE, 1)
    r8b:RegisterDataType = ("r8b", MemorySize.BYTE, 0)
    r9b:RegisterDataType = ("r9b", MemorySize.BYTE, 0)
    r10b:RegisterDataType = ("r10b", MemorySize.BYTE, 0)
    r11b:RegisterDataType = ("r11b", MemorySize.BYTE, 0)

    @classmethod
    def from_size(cls, size:MemorySize) -> (RegisterData, RegisterData):
        RD = RegisterData
        match size:
            case MemorySize.BYTE:
                return RD.ah, RD.al
            case MemorySize.WORD:
                return RD.dx, RD.ax
            case MemorySize.DWORD:
                return RD.edx, RD.eax
            case MemorySize.QWORD:
                return RD.rdx, RD.rax

    @property
    def register_name(self) -> str:
        return self.value[0]

    @property
    def size(self) -> MemorySize:
        return self.value[1]

    @property
    def position(self) -> Literal[0]|Literal[1]:
        """
        return 0 if upper bytes, return 1 if lower bytes
        """
        return self.value[2]

class Register:
    data:RegisterData
    
    def __init__(self, register:str | RegisterData):
        self.data = RegisterData[register] if isinstance(register, str) else register

    @property
    def name(self) -> str:
        return self.data.register_name

    @property
    def size(self) -> MemorySize:
        return self.data.size

    @property
    def position(self) -> Literal[0]|Literal[1]:
        """
        return 0 if upper bytes, return 1 if lower bytes
        """
        return self.data.position

    def __eq__(self, other:Register):
        return self.size.value == other.size.value

    def __gt__(self, other:Register):
        return self.size.value > other.size.value

    def __lt__(self, other:Register):
        return self.size.value > other.size.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"({self.name}[{self.size}] : {'lower' if self.position else 'upper'})"

InstructionDataType = tuple[str, list[list[MemorySize|type|int]], list[MemorySize|type|int|str|tuple[str,str]|None|Block]]
#                          [name, argument permutations (literal integers identify a wildcard size match group), return memory (None means for all permutations, value of str of num means use the same size as that index in the permutation; if str is reg name it loads into that specific reg; val of None means unknown)]

class OffsetRegister(Register):
    def __init__(self, register:Register, offset:str):
        self.register = register
        self.offset = offset

    @property
    def name(self):
        return self.register.name

    @property
    def size(self):
        return self.register.size

    @property
    def position(self):
        return self.register.position

    def __str__(self)->str:
        return f"{self.size.name}[{self.name}+{self.offset}]"

class Variable:
    def __init__(self, name:str, size:MemorySize, value:list|int = None):
        self.name = name
        self.size = size
        self.value = value
        self.empty = isinstance(self.value, int)
        
    def write(self) -> str:
        return str(self)
    def __str__(self)->str:
        return f"{self.size.name}[{self.name}]"
    def __getitem__(self, offset:str) -> Variable|OffsetVariable:
        return OffsetVariable(self, offset)

    def declare(self):
        return f"{self.name} {self.size.sec_bss_write if self.empty else self.size.sec_data_write} " + ", ".join(str(a) for a in self.value)


class OffsetVariable(Variable):
    def __init__(self, variable:Variable, offset:str):
        self.variable = variable
        self.offset = offset

    @property
    def name(self):
        return self.variable.name

    @property
    def size(self):
        return self.variable.size

    @property
    def value(self):
        return self.variable.value

    def __str__(self)->str:
        return f"{self.size.name}[{self.name}+{self.offset}]"

#redefine enum meta to handle builtin enum names
class InstructionDataEnumMeta(EnumMeta):
    def __getitem__(cls, name):
        return super().__getitem__(
            f"{name}_" if 
            name in {"and", "or", "not", "int"}
            else name
        )

class InstructionData(Enum, metaclass=InstructionDataEnumMeta):
    # this class's enums contains sizes, number of args etc to validate instructions
    mov:InstructionDataType = ("mov", [[0, 1], [0, int], [0, str]], [0,0,0])
    movsx:InstructionDataType = ("movsx", [[0, 1], [0, int], [0, str]], [0,0,0])
    movzx:InstructionDataType = ("movzx", [[0, 1], [0, int], [0, str]], [0,0,0])
    add:InstructionDataType = ("add", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    sub:InstructionDataType = ("sub", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])

    mul:InstructionDataType = ("mul", [[0], [int], [str]], ["0", None, None])
    div:InstructionDataType = ("div", [[0], [int], [str]], [("0","0"),None,None])

    imul:InstructionDataType = ("imul", [[0, 0, 0], [0, 0, int], [0, 0, str],[0, 0], [0, int], [0, str], [0], [int], [str]], ["0", "0", "0", "0", "0", "0","0", None, None])
    idiv:InstructionDataType = ("idiv", [[0], [int], [str]], [("0","0"),None,None])

    inc:InstructionDataType = ("inc", [[0]], [0])
    dec:InstructionDataType = ("dec", [[0]], [0])
    syscall:InstructionDataType = ("syscall", [[]], [])
    ret:InstructionDataType = ("ret", [[]], [])

    push:InstructionDataType = ("push", [[MemorySize.QWORD]], [None])
    pop:InstructionDataType = ("pop", [[MemorySize.QWORD]], [None])
    
    cmp:InstructionDataType = ("cmp", [[0, 0], [0, int], [0, str]], [0,0,0])
    and_:InstructionDataType = ("and", [[0, 0], [0, int], [0, str]], [0,0,0])
    or_:InstructionDataType = ("or", [[0, 0], [0, int], [0, str]], [0,0,0])
    xor:InstructionDataType = ("xor", [[0, 0], [0, int], [0, str]], [0,0,0])
    not_:InstructionDataType = ("not", [[0]], [0])
    neg:InstructionDataType = ("neg", [[0]], [0])
    shl:InstructionDataType = ("shl", [[0, 0], [0, int], [0, str]], [0,0,0])
    shr:InstructionDataType = ("shr", [[0, 0], [0, int], [0, str]], [0,0,0])
    sar:InstructionDataType = ("sar", [[0, 0], [0, int], [0, str]], [0,0,0])
    rol:InstructionDataType = ("rol", [[0, 0], [0, int], [0, str]], [0,0,0])
    ror:InstructionDataType = ("ror", [[0, 0], [0, int], [0, str]], [0,0,0])

    call:InstructionDataType = ("call", [[Block]], [Block])
    jmp:InstructionDataType = ("jmp", [[Block]], [Block])
    loop:InstructionDataType = ("loop", [[Block]], [Block])
    jne:InstructionDataType = ("jne", [[Block]], [Block])
    jle:InstructionDataType = ("jle", [[Block]], [Block])
    jl:InstructionDataType = ("jl", [[Block]], [Block])
    jge:InstructionDataType = ("jge", [[Block]], [Block])
    jg:InstructionDataType = ("jg", [[Block]], [Block])
    je:InstructionDataType = ("je", [[Block]], [Block])

    lea:InstructionDataType = ("lea", [[0,1]], [0])

    nop:InstructionDataType = ("nop", [[]], [])
    clc:InstructionDataType = ("clc", [[]], [])
    stc:InstructionDataType = ("stc", [[]], [])
    cld:InstructionDataType = ("cld", [[]], [])
    std:InstructionDataType = ("std", [[]], [])
    rep:InstructionDataType = ("rep", [[]], [])
    int_:InstructionDataType = ("int", [[int], [str]], [None,None])

    
    @property
    def instruction_name(self) -> str:
        return self.value[0]

    @property
    def arguments(self) -> list[MemorySize|type|int|str|tuple[str,str]|None|Variable]:
        return self.value[1]

    @property
    def ret_key(self) -> list[MemorySize|type|int|str|tuple[str,str]|None|Variable]:
        return self.value[2]



class Instruction:
    def __init__(self, instruction:str|InstructionData, *arguments:list[Register|str|int|Variable|Block]):
        self.data = InstructionData[instruction] if isinstance(instruction, str) else instruction
        self.arguments = arguments
        self.err_msg = None
        self.__ret = None
        if not self:
            raise SyntaxError(f"Invalid instruction: \"{self}\".\nReason: {self.err_msg}")

    @property
    def name(self) -> str:
        return self.data.instruction_name

    def __str__(self):
        return f"{self.name} " + ", ".join(str(a) for a in self.arguments)

    def write(self):
        if not self:
            raise SyntaxError(f"Invalid instruction: \"{self}\".\nReason: {self.err_msg}")
        return str(self)

    def __bool__(self) -> bool:
        """
        This is where the instruction arguments are validated.
        """
        for arg_perm in self.data.arguments:
            if len(arg_perm) != len(self.arguments):
                continue

            arg_groups = {}
            for a_n, arg in enumerate(self.arguments):
                self.__ret = self.__get_ret(a_n)
                if arg_perm[a_n] is int:
                    if not isinstance(arg, int):
                        if not self.err_msg:
                            self.err_msg = f"Argument #{a_n+1} was expected to be a literal int. Got: {arg!r}"
                        break

                elif arg_perm[a_n] is str:
                    if not isinstance(arg, str):
                        if not self.err_msg:
                            self.err_msg = f"Argument #{a_n+1} was expected to be a literal str. Got: {arg!r}"
                        break

                elif isinstance(arg_perm[a_n], int):
                    if arg_perm[a_n] not in arg_groups:
                        if hasattr(arg, "size"):
                            arg_groups[arg_perm[a_n]] = arg.size
                        else:
                            if not self.err_msg:
                                self.err_msg = f"Argument #{a_n+1} was expected to be a sized type. Got: {arg!r}"
                            break
                        # break means fail and go to the next argument permutation
                    elif hasattr(arg, "size") and arg_groups[arg_perm[a_n]] == arg.size:
                        continue
                    else:
                        if not self.err_msg:
                            self.err_msg = f"Argument #{a_n+1} was expected to be a {arg_groups[arg_perm[a_n]]!r}. Got: {arg!r}"
                        break

                elif isinstance(arg_perm[a_n], MemorySize):
                    if hasattr(arg, "size"):
                        if arg_perm[a_n] != arg.size:
                            if not self.err_msg:
                                self.err_msg = f"Argument #{a_n+1} was expected to be of size {arg_perm[a_n]!r}. Got: {arg.size!r}"
                            break
                    else:
                        if not self.err_msg:
                            self.err_msg = f"Argument must be sized and #{a_n+1} was expected to be of size {arg_perm[a_n]!r}. Got: {arg!r}"
                            break
            else:return True

        return False

    def __get_ret(self, r_ind:int):
        index = self.data.ret_key[r_ind]

        if isinstance(index, int):
            if hasattr(self.arguments[index], "size"):
                return self.arguments[index]
        elif isinstance(index, str):
            int_ind = int(index)
            if hasattr(self.arguments[int_ind], "size"):
                return Register(RegisterData.from_size(self.arguments[int_ind].size))
        elif isinstance(index, tuple):
            ind_1, _ = tuple(int(i) for i in index)
            if hasattr(self.arguments[ind_1], "size"):
                if self.data.instruction_name in {"div", "idiv"}:
                    return tuple(Register(r) for r in
                        RegisterData.from_size(self.arguments[ind_1].size.shrink))
                return tuple(Register(r) for r in RegisterData.from_size(self.arguments[ind_1].size))
        return None


    def __call__(self, recorder:Program|None = None):
        if not self:
            raise SyntaxError(f"Invalid instruction: \"{self}\".\nReason: {self.err_msg}")
        (recorder if recorder else Program.CURRENT).append(self)
        return self.__ret

class Function(Block):
    # None argument gets casted to 64 bit and pushed/popped to the stack
    def __init__(self, arguments:list[Register|None], signed_args:set[int]|None = None, return_register:Register|None = None, label:str|None = None):
        super().__init__(label)
        self.arguments = []
        self.stack_offset = -8
        self.signed_args = {} if signed_args is None else signed_args
        self.return_register = return_register
        for arg in arguments:
            if arg is None:
                self.stack_offset += 8
                self.arguments.append(OffsetRegister(Register("rsp"), self.stack_offset))
            else:
                self.arguments.append(arg)

    def __str__(self):
        return f"{self.label}"

    def write(self):
        return f"    global {self}\n{self}:\n    push rbp"

    def __call__(self, recorder:Program|None = None):
        (recorder if recorder else Program.CURRENT).append(self)
        return self

    def ret(self):
        Instruction("pop", Register("rbp"))()
        Instruction("ret")()

    def call(self, *arguments:list) -> Register|None:
        if len(list(filter(lambda a:not isinstance(a, OffsetRegister), self.arguments))) != len(self.arguments):
            Instruction("sub", Register("rsp"), 32)()
        for a_n, arg in reversed(list(enumerate(self.arguments))):
            if isinstance(arg, Register):
                if arg > arguments[a_n]:
                    Instruction("movsx" if a_n in self.signed_args else "movzx", arg, arguments[a_n])()
                else:
                    Instruction("mov", arg, arguments[a_n])()

            elif isinstance(arg, OffsetRegister):
                if arg > arguments[a_n]:
                    Instruction("movsx" if a_n in self.signed_args else "movzx", arg, arguments[a_n])()
                else:
                    Instruction("mov", arg, arguments[a_n])()

        Instruction("call", self)()
        return self.return_register

class Memory:
    def __init__(self, text_inclusions:list[str]|None=None, **memory:dict[str, tuple[MemorySize|str, list[any]|int]]):
        self.data = {}
        self.bss = {}
        self.variables = {}
        self.text_inclusions = [] if text_inclusions is None else text_inclusions
        for label, val in memory.items():
            val_new = val if isinstance(val[0], MemorySize) else (MemorySize[val[0]], val[1])
            if isinstance(val_new[1], int):
                self.bss[label] = val_new
            elif isinstance(val_new[1], list):
                self.data[label] = val_new

            self.variables[label] = Variable(label, *val_new)

    def __getitem__(self, value:str) -> Variable:
        return self.variables[value]

    def __str__(self):
        return (
            "section .data\n    "+
            "\n    ".join(
                f"{label} {size.sec_data_write} " + ", ".join(str(a) for a in arguments)
                for label, (size, arguments) in self.data.items()
            ) + "\n"+
            ("section .bss\n    " if self.bss else "")+
            "\n    ".join(
                f"{label} {size.sec_bss_write} {arguments}"
                for label, (size, arguments) in self.bss.items()
            ) + "\nsection .text\n    " +
            "\n    ".join(self.text_inclusions)
        )

    def write(self) -> str:
        return str(self)

    def __call__(self, recorder:Program|None = None):
        (recorder if recorder else Program.CURRENT).append(self)
        return self


                
if __name__ == "__main__":
    Reg = Register
    RegD = RegisterData
    Ins = Instruction
    InsD = InstructionData
    
    ah = Reg("ah")
    al = Reg("al")
    dx = Reg("dx")
    ax = Reg("ax")
    edx = Reg("edx")
    eax = Reg("eax")
    rdx = Reg("rdx")
    rax = Reg("rax")
    rdi = Reg("rdi")

    Program.CURRENT.name = "test"

    mem = Memory(["global _start"],
        apples = ("WORD", [3])
    )()

    Program.CURRENT.new_line()
    Program.CURRENT.comment("Function start:")
    #function start
    func_add_3_300 = Function([ax], return_register=ax, label="func_add_3_300")()

    Program.CURRENT.new_line()

    loop_block = Block()()

    ret_add = Ins("add", func_add_3_300.arguments[0], 3)()

    
    cmp = Ins("cmp", ret_add, 300)()
    jmp = Ins("jne", loop_block)()

    Program.CURRENT.new_line()

    func_add_3_300.ret()
    #function end
    Program.CURRENT.comment("Function end!")
    Program.CURRENT.new_line()

    start_block = Block("_start")()

    f_ret = func_add_3_300.call(mem["apples"])

    Ins('mov',mem["apples"], f_ret)()

    Program.CURRENT.new_line()
    Program.CURRENT.comment("Exit Program")
    Program.CURRENT.exit_program()

    Program.CURRENT.run()
