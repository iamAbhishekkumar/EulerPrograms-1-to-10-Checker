import git
import re
from os import listdir, curdir
from os.path import isfile, join, splitext

import requests

from dictionaries import language, euler_answer


def compileCode(_lang, _code, _input="", save=False):
    compile_url = "https://ide.geeksforgeeks.org/main.php"
    data = {
        'lang': _lang,
        'code': _code,
        'input': _input,
        'save': save,
    }
    request = requests.post(url=compile_url, data=data)
    code_sid = request.json()['sid']
    return code_sid


def getting_response(uid):
    submit_url = "https://ide.geeksforgeeks.org/submissionResult.php"
    submit_data = {
        'sid': uid,
        'requestType': "fetchResults"
    }
    submit = requests.post(url=submit_url, data=submit_data)
    return submit.json()


def getting_file_language(file_name):
    name, file_extension = splitext(file_name)
    return file_extension


def checker(repo_link):
    # Getting files from Repo
    cloned_repo_dir = curdir + "/answers"
    try:
        git.Repo.clone_from(url=repo_link, to_path=cloned_repo_dir)
    except git.exc.GitCommandError:
        pass
    finally:
        files = [f for f in listdir(cloned_repo_dir) if isfile(join(cloned_repo_dir, f))]
        filename_with_number = []
        for filename in files:
            num = re.findall(r'\d', filename)
            if len(num) >= 1:
                num = "".join(num)
                try:
                    filename_with_number.append([filename, num])
                except KeyError:
                    pass

        # extracting required results
        result = []
        for i in filename_with_number:
            if int(i[1]) <= 10:
                filename = "answers/" + i[0]
                print(filename + ".........")
                code_file = open(filename, "r")
                code = code_file.read()
                lang = language[getting_file_language(filename)]
                uid = compileCode(lang, code)
                flag = 0
                output, error = None, None
                while flag == 0:
                    response = getting_response(uid)
                    status = response['status']
                    try:
                        output = response['output']
                    except KeyError:
                        pass
                    try:
                        error = response['cmpError']
                    except KeyError:
                        pass
                    if status == "SUCCESS" and output is not None:
                        try:
                            time = getting_response(uid)['time']
                            result.append([output, euler_answer[i[1]], i[0], float(time)])
                        except KeyError:
                            pass
                        flag = 1
                    elif status == "SUCCESS" and error is not None:
                        result.append(["Compile Error", i[0]])
                        flag = 1
    return result
