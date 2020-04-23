#!/usr/bin/env python

def get_collision_dict(file_name):
    collision_file = open(file_name, "r")
    collisions = {}
    for line in collision_file:
        line = line.strip()
        if line.startswith("<disable_collisions"):
            line = line.split()
            link_1 = line[1].split("=")[1][1:-1]
            link_2 = line[2].split("=")[1][1:-1]
            if not collisions.has_key(link_1):
                collisions[link_1] = [link_2]
            else:
                if link_2 not in collisions[link_1]:
                    collisions[link_1].append(link_2)
            if not collisions.has_key(link_2):
                    collisions[link_2] = [link_1]
            else:
                if link_2 not in collisions[link_2]:
                    collisions[link_2].append(link_1)
    
    collision_file.close()
    return collisions

def has_pair(collision, link_1, link_2):
    return collision.has_key(link_1) and link_2 in collision[link_1]

current_collisions = get_collision_dict("baxter.srdf")
other_collisions = get_collision_dict("other_collisions.xml")

collisions_to_add = {}

for link in other_collisions.keys():
    if not current_collisions.has_key(link):
        if not collisions_to_add.has_key(link):
            collisions_to_add[link] = [i for i in other_collisions[link]]
        else:
            for i in other_collisions[link]:
                if i not in collisions_to_add[link]:
                    collisions_to_add[link].append(i)
    else:
        for link_2 in other_collisions[link]:
            if link_2 not in current_collisions[link]:
                if (not has_pair(collisions_to_add, link, link_2)) and (not has_pair(collisions_to_add, link_2, link)):
                    if collisions_to_add.has_key(link):
                        collisions_to_add[link].append(link_2)
                    else:
                        collisions_to_add[link] = [link_2]

lines = []
for link_1 in collisions_to_add.keys():
    for link_2 in collisions_to_add[link_1]:
        line = '    <disable_collisions link1="' + link_1 + '" link2="' + link_2 + '" reason="Never" />'
        lines.append(line)
        print line
    #print link, ": ", collisions_to_add[link]
                    