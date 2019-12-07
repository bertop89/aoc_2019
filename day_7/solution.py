def get_modes(op_code_str):
    return int(op_code_str[1]), int(op_code_str[2])


def get_operators(input_list, first_mode, second_mode, i):
    first_op = input_list[i + 1] if first_mode == 1 else input_list[input_list[i + 1]]
    try:
        second_op = input_list[i + 2] if second_mode == 1 else input_list[input_list[i + 2]]
    except:
        second_op = -1
    try:
        output_id = input_list[i + 3]
    except:
        output_id = -1
    return first_op, second_op, output_id


def program_alarm(input_list_2, input_1, input_2, i=0):
    input_list = input_list_2[:]
    while i < len(input_list):
        op_code_str = str(input_list[i]).zfill(5)
        op_code = int(op_code_str[-2:])
        if op_code == 99:
            break

        second_mode, first_mode = get_modes(op_code_str)
        first_op, second_op, output_id = get_operators(input_list, first_mode, second_mode, i)
        if op_code <= 2:
            if op_code == 1:
                result = first_op + second_op
            elif op_code == 2:
                result = first_op * second_op
            input_list[output_id] = result
            i += 4
        elif op_code <= 4:
            if op_code == 3:
                input_list[input_list[i + 1]] = input_1
                input_1 = input_2
            elif op_code == 4:
                return first_op, input_list, i+2
            i += 2
        elif op_code <= 6:
            if op_code == 5:
                if first_op != 0:
                    i = second_op
                else:
                    i += 3
            elif op_code == 6:
                if first_op == 0:
                    i = second_op
                else:
                    i += 3
        elif op_code <= 8:
            if op_code == 7:
                if first_op < second_op:
                    input_list[output_id] = 1
                else:
                    input_list[output_id] = 0
            elif op_code == 8:
                if first_op == second_op:
                    input_list[output_id] = 1
                else:
                    input_list[output_id] = 0
            i += 4

        else:
            break

    return None, input_list, i+1


def compute_amplifiers(program, phase_setting):
    output, _, _ = program_alarm(program, int(phase_setting[0]), 0)
    for current_setting in phase_setting[1:]:
        output, _, _ = program_alarm(program, int(current_setting), output)
    return output

test_program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
print(compute_amplifiers(test_program, '43210'))

test_program_2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
print(compute_amplifiers(test_program_2, '01234'))

test_program_3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
print(compute_amplifiers(test_program_3, '10432'))

from itertools import permutations

def compute_highest_signal(program, permutation='012345', function=compute_amplifiers):
    max_output = 0
    max_setting = None
    for permutation in permutations(permutation, 5):
        current_setting = ''.join(permutation)
        output = function(program, current_setting)
        if output > max_output:
            max_output = output
            max_setting = current_setting
    return max_setting, max_output

print(compute_highest_signal(test_program))
print(compute_highest_signal(test_program_2))
print(compute_highest_signal(test_program_3))

# part 1
input_program = [3,8,1001,8,10,8,105,1,0,0,21,46,67,88,101,126,207,288,369,450,99999,3,9,1001,9,5,9,1002,9,5,9,1001,9,5,9,102,3,9,9,101,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,5,9,9,101,3,9,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,102,3,9,9,1001,9,4,9,4,9,99,3,9,102,3,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99]
print(compute_highest_signal(input_program))


# part 2
from itertools import cycle

def compute_looped_amplifiers(initial_program, phase_setting):
    memory = {}
    exit_on_next = False
    output, program, pointer = program_alarm(initial_program, int(phase_setting[0]), 0)
    memory[phase_setting[0]] = (program, pointer)
    for current_setting in cycle(phase_setting[1:] + phase_setting[:1]):
        current_program, pointer = memory[current_setting] if current_setting in memory else (initial_program, 0)
        if pointer == 0:
            current_input = int(current_setting)
        else:
            current_input = output
        current_output, program, pointer = program_alarm(current_program, current_input, output, pointer)
        if exit_on_next and current_setting == phase_setting[-1]:
            return output
        if current_output is None:
            exit_on_next = True
        else:
            output = current_output
            memory[current_setting] = (program, pointer)
    return output

test_program_4 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
print(compute_looped_amplifiers(test_program_4, '98765'))
print(compute_highest_signal(test_program, permutation='56789', function=compute_looped_amplifiers))

test_program_5 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
print(compute_looped_amplifiers(test_program_5, '97856'))
print(compute_highest_signal(test_program_5, permutation='56789', function=compute_looped_amplifiers))

print(compute_highest_signal(input_program, permutation='56789', function=compute_looped_amplifiers))





