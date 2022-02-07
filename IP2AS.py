# Programming Assignment 1
# We have to longest IP index match the input IP address with all the IPs in the DB.txt file given
# Once we find the correct match, return the correct match and offset and original IP.
# Ex: 
# Input: 12.105.69.152  Output: 12.105.69.144/28 15314 12.105.69.152

# Harrod Tang, Nathaniel Faxon

import sys
import copy

#convert CIDR IP addr to binary
def convert_binary(ip_address):
    ret_string = str()
    parsed_ip = ip_address.split(".")
    for i in range(len(parsed_ip)):
        parsed_ip[i] = '{0:08b}'.format( int(parsed_ip[i]) )
        ret_string += str(parsed_ip[i]) + "."
    # print(ret_string[:-1])
    return ret_string[:-1]

#convert binary IP addr back to CIDR
def convert_to_decimal(ip_address):
    ret_string = str()
    parsed_ip = ip_address.split(".")
    for i in range(len(parsed_ip)):
        parsed_ip[i] = int(parsed_ip[i], 2)
        ret_string += str(parsed_ip[i]) + "."
    # print(ret_string[:-1])
    return ret_string[:-1]

# masks any bits after subnet mask with '*'
def mask_ip_address(ip_address, subnet_mask):
    ret_string = str()
    subnet_mask = int(subnet_mask)    
    num_dots = subnet_mask // 8
    if subnet_mask == 32:
        num_dots = 3
    subnet_mask += num_dots
    
    count = 0
    for bit in ip_address:
        if count >= subnet_mask and bit != ".":
            ret_string += "*"
        else:
            ret_string += bit
        count += 1
    return ret_string

def get_list_of_matching_indices(index_txt):
    ret_list = []

    for i in range(len(input_txt)):
        input_txt[i] = convert_binary(input_txt[i])
    
    for i in range(len(input_txt)):
        max_match_index = 0
        max_matches = 0
        input_ip = input_txt[i]
        for j in range(len(routing_table)):
            num_matches = 0
            is_valid_match = 0
            for k in range(35):
                if input_ip[k] == routing_table[j][0][k]:
                    num_matches += 1
                    is_valid_match = 1
                else:
                    if routing_table[j][0][k+1] != "*":
                        is_valid_match = 0
                    break

            if num_matches >= max_matches and is_valid_match:                    
                max_matches = num_matches
                max_match_index = j
        ret_list.append(max_match_index)

    return ret_list

if __name__ == "__main__":
    #Parse the input text files
    arg_length = len(sys.argv)
    if arg_length != 3:
        print("Incorrect # of inputs")
        exit()

    #Open the DB txt, strip white spaces, split element into list
    with open(sys.argv[1]) as f:
        routing_table = f.readlines()
    
    for i in range(len(routing_table)):
        if routing_table[i] == "" or routing_table[i] == "\n":
            routing_table.remove(routing_table[i])

    for i in range(len(routing_table)):
        routing_table[i] = routing_table[i].rstrip("\n")
        routing_table[i] = routing_table[i].split()

    #Create copy of the DB txt for printing to output txt
    routing_table_copy = copy.deepcopy(routing_table)

    #Open the input txt and strip white spaces
    with open(sys.argv[2]) as f:
        input_txt = f.readlines()

    for i in range(len(input_txt)):
        input_txt[i] = input_txt[i].rstrip("\n")
    
    #Create copy of the input txt for printing to output txt
    input_copy = copy.deepcopy(input_txt)

    #Convert element from routing_table from decimal to binary
    for i in range(len(routing_table)):
        #print("i: ", i)
        routing_table[i][0] = convert_binary(routing_table[i][0])
    
    #Convert digits past subnet value to *
    for i in range(len(routing_table)):
        ip_addr = routing_table[i][0]
        offset = routing_table[i][1]
        
        routing_table[i][0] = mask_ip_address(ip_addr, offset)
    
    #Convert element in input txt to binary
    match_indices = get_list_of_matching_indices(input_txt)
    
    count = 0
    with open("output.txt", 'w') as file:
        for element in match_indices:
            ip_addr = routing_table_copy[element][0]
            subnet_mask = routing_table_copy[element][1]
            as_number = routing_table_copy[element][2]

            print_string = ip_addr + "/" + subnet_mask + " " + as_number + " " + input_copy[count]
            count += 1

            file.write(print_string + "\n")
        
    file.close

