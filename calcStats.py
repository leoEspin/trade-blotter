#!/usr/bin/env python3

import argparse


def parcero():
    huyparce = argparse.ArgumentParser()
    huyparce.add_argument('-i', '--input', type=str,
                          metavar='input.csv', required=True)
    huyparce.add_argument('-o', '--output', type=str,
                          metavar='output.csv')
    return huyparce.parse_args()

def csv_reader(file_name):
    lines = (line for line in open(file_name))
    list_line = (s.rstrip().split(",") for s in lines) 
    cols = next(list_line)
    for row in list_line:
        yield row
        
def logic(row: list, groud_truth: dict)-> dict:
    tail = [0] * 10
    row[4] = int(row[4])
    row[5] = float(row[5])
    tail[3] = row[4] * row[5]
    if row[3] == 'b':
        if row[1] not in groud_truth.keys():
            groud_truth[row[1]] = row[4]
            tail[0] = row[4]
        else:
            groud_truth[row[1]] += row[4]
            tail[0] += row[4]
        if row[6] not in groud_truth.keys():
            groud_truth[row[6]] = {'b': row[4], 's': 0}
        else:
            groud_truth[row[6]]['b'] += row[4]            
    else: 
        if row[1] not in groud_truth.keys():
            groud_truth[row[1]] = -row[4]
            tail[1] = row[4]
        else:
            groud_truth[row[1]] -= row[4]
            tail[1] += row[4]
        if row[6] not in groud_truth.keys():
            groud_truth[row[6]] = {'b': 0, 's': row[4]}
        else:
            groud_truth[row[6]]['s'] += row[4]  
    tail[2] = groud_truth[row[1]]
    tail[4] = groud_truth[row[6]]['b']
    tail[5] = groud_truth[row[6]]['s']
    return tail, groud_truth

def calcTradeStats(input:str, output: str):
    the_truth = {}
    for row in csv_reader(input):
        extended, the_truth = logic(row, the_truth)
        print(row + extended)    

if __name__ == '__main__':
    args = parcero()
    calcTradeStats(args.input, args.output)
