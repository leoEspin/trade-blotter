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
        
def logic(row: list, groud_truth: dict, exchanges: list)-> dict:
    '''
    ground_truth contains the current number of shares of a given symbol (SymbolPosition),
    and the number of shares bought and sold in a given exchange (ExchangeBought, 
    ExchangeSold)
    schema:
    {symbol: {'current': shares, 'b': shares, 's': shares},
    exchange: {'b': shares, 's':shares}}
    '''
    tail = [0] * 10
    row[4] = int(row[4])
    row[5] = float(row[5])

    if row[3] == 'b':   
        sign = 1
    else:
        sign = -1
    bfactor = int(sign > 0)
    sfactor = int(sign < 0)
    if row[1] not in groud_truth.keys():
        groud_truth[row[1]] = {
            'c': sign * row[4],
            'b': bfactor * row[4], 
            's': sfactor * row[4]}
    else:
        groud_truth[row[1]]['c'] += sign * row[4]
        groud_truth[row[1]]['b'] += bfactor * row[4]
        groud_truth[row[1]]['s'] += sfactor * row[4]

    if row[6] not in groud_truth.keys():
        groud_truth[row[6]] = {'b': bfactor * row[4], 's': sfactor * row[4]}
        exchanges.append(row[6])
    else:
        groud_truth[row[6]]['b'] += bfactor * row[4]
        groud_truth[row[6]]['s'] += sfactor * row[4]

    tail[0] = groud_truth[row[1]]['b']
    tail[1] = groud_truth[row[1]]['s']   
    tail[2] = groud_truth[row[1]]['c'] 
    tail[3] = row[4] * row[5]
    tail[4] = groud_truth[row[6]]['b']
    tail[5] = groud_truth[row[6]]['s']
    tail[6] = sum(groud_truth[ex]['b'] for ex in exchanges)
    tail[7] = sum(groud_truth[ex]['s'] for ex in exchanges)     
    return tail, groud_truth, exchanges

def calcTradeStats(input:str, output: str):
    the_truth = {}
    exchanges = []
    for row in csv_reader(input):
        extended, the_truth, exchanges = logic(row, the_truth, exchanges)
        print(row + extended)    
    return the_truth

if __name__ == '__main__':
    args = parcero()
    out = calcTradeStats(args.input, args.output)
    print(out)
