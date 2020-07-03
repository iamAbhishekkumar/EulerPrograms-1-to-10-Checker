from os import curdir, mkdir, path, walk, chmod
from re import findall
import stat
import code_checker as cc
import shutil

cloned_repo_dir = curdir + "/answers"

# deleting answer contents before cloning another repo
if path.exists(cloned_repo_dir):
    for root, dirs, files in walk(cloned_repo_dir):
        for dir in dirs:
            chmod(path.join(root, dir), stat.S_IRWXU)
        for file in files:
            chmod(path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(cloned_repo_dir)
    mkdir(cloned_repo_dir)

github_repo_link = input("Enter the repo link : ")
result = cc.checker(github_repo_link)

wrong_answer = []
correct_answer = []
total_time = 0

for i in result:
    try:
        if i[0] == "Compile Error":
            wrong_answer.append("Error type : " +i[0]+" in question "+i[1])
        elif "".join(findall(r'\d', i[0])) != i[1]:
            total_time += i[3]
            correct_answer.append("yes")

    except IndexError:
        pass

if len(correct_answer) == 10 and total_time <= 5:
    print("All are correct answers")
elif total_time > 4:
    print("Program takes too much time...")
else:
    if len(wrong_answer) == 0:
        print("Some questions files may be missing.....")
    else:
        print("Following question number are wrong : ")
        for _ in wrong_answer:
            print(_)
