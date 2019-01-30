#!/usr/bin/env python3
import xlrd
import os.path as p

if __name__ == "__main__":
    script_path = p.dirname(p.abspath(__file__))
    book = xlrd.open_workbook(p.join(script_path, 'chess.xlsx'))
    sheet = book.sheet_by_index(0)
    print(sheet.name)

    class_map = {'n':0}
    species_map = {'n':0}
    chess_map = {}
    for r in range(1, sheet.nrows):
        chess_cell = sheet.cell(r, 1)
        if chess_cell.ctype == xlrd.XL_CELL_EMPTY: continue

        class_cell = sheet.cell(r, 4)
        class_value = -1
        if class_cell.ctype != xlrd.XL_CELL_EMPTY:
            cell_value = class_cell.value # type: str
            cell_value = cell_value.strip()
            if cell_value in class_map:
                class_value = class_map[cell_value]
            else:
                class_map[cell_value] = class_value = class_map['n']
                class_map['n'] += 1

        species_list = []
        for c in [2,3]:
            species_cell = sheet.cell(r, c)
            species_value = -1
            if species_cell.ctype != xlrd.XL_CELL_EMPTY:
                cell_value = species_cell.value  # type: str
                cell_value = cell_value.strip()
                if cell_value in species_map:
                    species_value = species_map[cell_value]
                else:
                    species_map[cell_value] = species_value = species_map['n']
                    species_map['n'] += 1
                species_list.append(species_value)
        chess_map[str(chess_cell.value).strip()] = [class_value, species_list]
    del class_map['n']
    del species_map['n']
    print(chess_map)
    print(class_map)
    print(species_map)

    fp_class = open(p.join(script_path, 'dota_class.dot'), 'w+')
    fp_species = open(p.join(script_path, 'dota_species.dot'), 'w+')
    fp_dota = open(p.join(script_path, 'dota.dot'), 'w+')

    def append_head(fp):
        fp.write('digraph\n{\n')
        fp.write('    bgcolor=transparent;\n')
        fp.write('    rankdir=LR;\n')
        fp.write('    graph[nodesep=0.1,ranksep=4,style=invis];\n')
        fp.write('    edge[arrowhead=none];\n')

    def append_class(fp):
        # class
        fp.write('    subgraph cluster_class {\n')
        for name, cid in class_map.items():
            fp.write('        c{}[label="{}"];\n'.format(cid, name))
        fp.write('    }\n')

    def append_chess(fp):
        # chess
        chess_index = 0
        fp.write('    subgraph cluster_chess {\n')
        for name, gset in chess_map.items():
            fp.write('{}h{}[label="{}"];\n'.format(' '*8, chess_index, name))
            chess_index += 1
        fp.write('    }\n')

    def append_species(fp):
        # species
        fp.write('    subgraph cluster_species {\n')
        for name, sid in species_map.items():
            fp.write('        s{}[label="{}"];\n'.format(sid, name))
        fp.write('    }\n')

    def append_connect_class(fp, reverse=True):
        # connect_class
        chess_index = 0
        fp.write('    subgraph cluster_chess_class {\n')
        for name, gset in chess_map.items():
            if reverse:
                fp.write('{}c{}->h{};\n'.format(' '*8, gset[0], chess_index))
            else:
                fp.write('{}h{}->c{};\n'.format(' ' * 8, chess_index, gset[0]))
            chess_index += 1
        fp.write('    }\n')

    def append_connect_species(fp, reverse=False):
        # connect_species
        chess_index = 0
        fp.write('    subgraph cluster_chess_species {\n')
        for name, gset in chess_map.items():
            for sid in gset[1]:
                if reverse:
                    fp.write('{}s{}->h{};\n'.format(' ' * 8, sid, chess_index))
                else:
                    fp.write('{}h{}->s{};\n'.format(' ' * 8, chess_index, sid))
            chess_index += 1
        fp.write('    }\n')

    def append_tail(fp):
        fp.write('}\n')

    def dump(fp):
        fp.seek(0)
        print('[DUMP] {}'.format(fp.name))
        print(fp.read())

    # class
    append_head(fp=fp_class)
    append_class(fp=fp_class)
    append_chess(fp=fp_class)
    append_connect_class(fp=fp_class, reverse=True)
    append_tail(fp=fp_class)
    dump(fp=fp_class)

    # species
    append_head(fp=fp_species)
    append_species(fp=fp_species)
    append_chess(fp=fp_species)
    append_connect_species(fp=fp_species, reverse=True)
    append_tail(fp=fp_species)
    dump(fp=fp_species)

    # combination
    append_head(fp=fp_dota)
    append_species(fp=fp_dota)
    append_class(fp=fp_dota)
    append_chess(fp=fp_dota)
    append_connect_species(fp=fp_dota)
    append_connect_class(fp=fp_dota)
    append_tail(fp=fp_dota)
    dump(fp=fp_dota)

