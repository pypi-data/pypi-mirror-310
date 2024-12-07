#!/usr/bin/env python3
import os
import subprocess
import sys
import uuid
import time

t_start = time.time()

try:
    prtr_path = os.environ['PRAETOR']
    sys.path.append(prtr_path)
    import praetor_settings_user as praetor_settings

except:
    from praetor import praetor_settings
    # import praetor_settings
    pass

def generate_pipeline_id():
    '''
    Creates a unique id for a pipeline run which includes the praetor version
    :return: Unique id
    '''
    try:
        proc1 = subprocess.Popen(['pip', 'show', 'praetor'], stdout=subprocess.PIPE)
    except FileNotFoundError:
        try:
            proc1 = subprocess.Popen(['pip3', 'show', 'praetor'], stdout=subprocess.PIPE)
        except FileNotFoundError:
            proc1 = subprocess.Popen(['pip2', 'show', 'praetor'], stdout=subprocess.PIPE)

    proc2 = subprocess.Popen(['grep', 'Version'], stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close()
    out, err = proc2.communicate()
    out = out.decode("utf-8")
    praetor_version = out[out.find(': ') + 2: -1]

    pipeline_id = "praetor_{}_{}".format(praetor_version, uuid.uuid4())
    return pipeline_id


def escape_forbidden_characters(in_string):
    '''
    Escapes special characters from an input string to fit PROV-N
    :param in_string: String to escape characters within
    :return: Original string with escaped characters
    '''
    forbidden = "\\(=)|,:;[]"
    allowed_special = '/._-'
    no_forbidden = [x if x.isalnum() else '\\' + x if x in forbidden else x if x in allowed_special else '' for x in in_string]
    final_string = ''.join(no_forbidden)
    return final_string


pipeline_id = generate_pipeline_id()
os.environ['PRAETOR_pipeline_id'] = pipeline_id
currentDir = praetor_settings.provenance_directory + '{}/'.format(pipeline_id)
subprocess.call(['mkdir', currentDir])

with open(currentDir+'templateDictionary.py','w') as f:
    f.write('tempDict = {}')


from praetor import convert2prov, decorate, genBindings, praetorTemplates
from praetor.python_builtin_wrap_templateGen import createOpenTemplate

# import convert2prov, decorate, praetorTemplates
# from python_builtin_wrap_templateGen import createOpenTemplate

newDirectories = ['prov', 'json', 'templates', 'big_entities', 'function_store']
for name in newDirectories:
    try:
        subprocess.call(['mkdir', currentDir+name])
    except:
        print('Directory {} already exists'.format(name))

with open(currentDir+'json/'+praetor_settings.json_file,'w') as f:
    f.write("")

def exclude_internals(exclude, modules):
    '''
    Patch to exclude modules used by praetor from provenance recording. This limits the capabilities but stops bugs.
    A future solution would be to not record provenance when praetor is active, but that is difficult to determine.
    Perhaps a link in the stack between last usage being praetor module and all subsquent being something that praetor
    could have called?
    :param exclude: list of all possible internal modules
    :param modules: all user input modules
    :returns: refined list
    '''
    modules = [x for x in modules if x not in exclude]
    for ex_mod in exclude:
        modules = [x for x in modules if '.{}.'.format(ex_mod) not in x]
        modules = [x for x in modules if not x.startswith('{}.'.format(ex_mod))]
        modules = [x for x in modules if not x.endswith('.{}'.format(ex_mod))]
    return modules


mega_exclude = ['__builtin__',
           'Tester', '_thread', 'graphlib', 'scriptScript', '__future__', '_threading_local', 'grp',
           'scriptresubmitter',
           '_abc', '_tkinter', 'gzip', 'secrets', '_aix_support', '_tracemalloc', 'hashlib', 'select', '_ast', '_uuid',
           'heapq', 'selectors', '_asyncio', '_warnings', 'hmac', 'setuptools', '_bisect', '_weakref', 'html', 'shelve',
           '_blake2', '_weakrefset', 'http', 'shlex', '_bootlocale', '_xxsubinterpreters', 'idlelib', 'shutil',
           '_bootsubprocess', '_xxtestfuzz', 'imaplib', 'signal', '_bz2', '_zoneinfo', 'imghdr', 'site', '_codecs',
           'abc',
           'imp', 'smtpd', '_codecs_cn', 'aifc', 'importlib', 'smtplib', '_codecs_hk', 'antigravity', 'inspect',
           'sndhdr',
           '_codecs_iso2022', 'argparse', 'io', 'socket', '_codecs_jp', 'array', 'ipaddress', 'socketserver',
           '_codecs_kr',
           'ast', 'itertools', 'spwd', '_codecs_tw', 'asynchat', 'json', 'sqlite3', '_collections', 'asyncio',
           'keyword',
           'sre_compile', '_collections_abc', 'asyncore', 'latexWriter', 'sre_constants', '_compat_pickle', 'atexit',
           'lib2to3', 'sre_parse', '_compression', 'audioop', 'linecache', 'ssl', '_contextvars', 'base64', 'locale',
           'stat', '_crypt', 'bdb', 'logging', 'statistics', '_csv', 'binascii', 'lzma', 'string', '_ctypes', 'binhex',
           'mailbox', 'stringprep', '_ctypes_test', 'bisect', 'mailcap', 'struct', '_curses', 'builtins', 'marshal',
           'subprocess', '_curses_panel', 'bwd', 'math', 'sunau', '_datetime', 'bz2', 'mimetypes', 'symbol', '_decimal',
           'cProfile', 'mmap', 'symtable', '_distutils_hack', 'calendar', 'modulefinder', 'sys', '_elementtree', 'cgi',
           'multiprocessing', 'sysconfig', '_functools', 'cgitb', 'netrc', 'syslog', '_hashlib', 'chunk', 'nis',
           'tabnanny',
           '_heapq', 'cmath', 'nntplib', 'tarfile', '_imp', 'cmd', 'ntpath', 'telnetlib', '_io', 'code', 'nturl2path',
           'tempfile', '_json', 'codecs', 'numbers', 'termios', '_locale', 'codeop', 'opcode', 'test', '_lsprof',
           'collections', 'operator', 'tester', '_lzma', 'colorsys', 'optparse',
           'testing_prtr_packagetemplateDictionary',
           '_markupbase', 'compileall', 'os', 'textwrap', '_md5', 'concurrent', 'ossaudiodev', 'this',
           '_multibytecodec',
           'configparser', 'parser', 'threading', '_multiprocessing', 'contextlib', 'pathlib', 'time', '_opcode',
           'contextvars', 'pdb', 'timeit', '_operator', 'copy', 'periodic', 'tkinter', '_osx_support', 'copyreg',
           'pickle',
           'token', '_peg_parser', 'crypt', 'pickletools', 'tokenize', '_pickle', 'csv', 'pip', 'trace', '_posixshmem',
           'ctypes', 'pipes', 'traceback', '_posixsubprocess', 'curses', 'pkg_resources', 'tracemalloc', '_py_abc',
           'dataclasses', 'pkgutil', 'tty', '_pydecimal', 'datetime', 'platform', 'turtle', '_pyio', 'dbm', 'plistlib',
           'turtledemo', '_queue', 'decimal', 'poplib', 'types', '_random', 'difflib', 'posix', 'typing', '_sha1',
           'dis',
           'posixpath', 'unicodedata', '_sha256', 'distutils', 'pprint', 'unittest', '_sha3', 'doctest', 'profile',
           'urllib',
           '_sha512', 'email', 'provcall-NoWorkflow-save', 'uu', '_signal', 'encodings', 'pstats', 'uuid',
           '_sitebuiltins',
           'ensurepip', 'pty', 'valuefilemaker', '_socket', 'enum', 'pwd', 'venv', '_sqlite3', 'errno', 'py_compile',
           'warnings', '_sre', 'faulthandler', 'pyclbr', 'wave', '_ssl', 'fcntl', 'pydoc', 'weakref', '_stat',
           'filecmp',
           'pydoc_data', 'webbrowser', '_statistics', 'fileinput', 'pyexpat', 'wheel', '_string', 'fnmatch', 'pytest',
           'wsgiref', '_strptime', 'formatter', 'python_modules', 'xdrlib', '_struct', 'fractions', 'queue', 'xml',
           '_symtable', 'ftplib', 'quopri', 'xmlrpc', '_sysconfigdata__linux_x86_64-linux-gnu', 'functools',
           'random', 'xxlimited', '_sysconfigdata_x86_64_conda_cos6_linux_gnu', 'gc', 're', 'xxsubtype',
           '_sysconfigdata_x86_64_conda_linux_gnu', 'genBindings', 'readline', 'zerosigmaker', '_testbuffer',
           'genericpath', 'reprlib', 'zipapp', '_testcapi', 'getopt', 'resource', 'zipfile', '_testimportmultiple',
           'getpass', 'rlcompleter', 'zipimport', '_testinternalcapi', 'gettext', 'runpy', 'zlib', '_testmultiphase',
           'glob', 'sched', 'zoneinfo',
           'genBindings', 'praetor', 'convert2prov', 'decorate', 'praetorTemplates', 'praetor_settings',
           'praetor_settings_user', 'templateDictionary', 'python_modules', 'uuid4']

modules_original = praetor_settings.modules
modules_refined = exclude_internals(mega_exclude, modules_original)

if __name__ == '__main__':

    possible_scripts = [x for x in sys.argv if '.py' in x]
    exampleScript = possible_scripts[1]

    # exampleScript = sys.argv[1]

    with open(exampleScript,'r') as f:
        script = f.read()

    newName, commented_globals = decorate.decorateFile(exampleScript, modules=modules_refined,
                                                       wrap_open=praetor_settings.wrap_open)
    # functionCommands = ['python', newName]

    # if len(sys.argv) > 2:
    #     stringCommands = [str(x) for x in sys.argv[2:]]
    #     functionCommands.extend(stringCommands)

    functionCommands = [x.replace(exampleScript, newName) for x in sys.argv[1:]]

    if praetor_settings.wrap_open:
        createOpenTemplate()

    time_setup = time.time() - t_start
    t_se = time.time()

    with open(currentDir+'/console_output.log', 'wb') as f:
        process = subprocess.Popen(functionCommands, stdout=subprocess.PIPE)
        for c in iter(lambda: process.stdout.read(1), b""):
            try:
                sys.stdout.write(c.decode("utf-8"))
                f.write(c)
            except UnicodeDecodeError:
                try:
                    sys.stdout.reconfigure(encoding="utf-8")
                    f.write(c)
                except UnicodeDecodeError:
                    f.write('Console log line not recorded, unicode error')

    example_sep = praetorTemplates.variableSeparation(script)
    tot_sep_dict = {x[0]:[x[1],x[2]] for x in example_sep.values()}
    function_code = [x[3] for x in example_sep.values()]

    for counter,key in enumerate(example_sep.keys()):
        template_no_special = praetorTemplates.escape_forbidden_characters(example_sep[key][0])
        if not os.path.isfile(currentDir+'/templates/{}_template.provn'.format(template_no_special)):
            bundle, bundleStarted = praetorTemplates.generateBundle(example_sep[key], praetorTemplates.bundleStart,
                                                                    praetorTemplates.bundleEnd)
            with open(currentDir+'/templates/{}_template.provn'.format(template_no_special),'w') as f:
                f.write(bundle)

            with open(currentDir+'/templates/{}started_template.provn'.format(template_no_special),'w') as f:
                f.write(bundleStarted)

            with open(currentDir+'/function_store/{}_function.txt'.format(template_no_special),'w') as f:
                f.write(function_code[counter])

    subprocess.call(['mv', newName, currentDir])

    make_string = """
ts := $(shell /bin/date "+%Y%m%d%H%M%S")

build:
\tmvn clean install

merge:
\tfind ./prov/*.provn | sed "s/^/file, /; s/$$/, provn/" | provconvert -merge - -outfile mergey.provn

flatten:
\tprovconvert -infile mergey.provn -index -flatten -outfile flatten_file.provn

flattensvg:
\tprovconvert -infile mergey.provn -index -flatten -outfile flatten_file.svg
  
flattenpng:
\tprovconvert -infile mergey.provn -index -flatten -outfile flatten_file.png

flattenrdf:
\tprovconvert -infile mergey.provn -index -flatten -outfile flatten_file.rdf

flattenttl:
\tprovconvert -infile mergey.provn -index -flatten -outfile flatten_file.ttl    
    """

    t_run = time.time() - t_se
    t_r = time.time()
    if praetor_settings.build_prov:

        convert2prov.combine_prov(currentDir+'json/full_json.json', currentDir+'json/agent_json.json',
                                  currentDir+'templates/', currentDir+'mergey.provn', commented_globals)

        with open(currentDir+'Makefile', 'w') as f:
            f.write(make_string)

        if praetor_settings.flatten_prov:
            os.chdir(currentDir)
            subprocess.call(['make','flatten'])

    t_build = time.time() - t_r

timing_string = "set_up_time = {0}\nrun_time = {1}\nbuild_time = {2}".format(time_setup, t_run, t_build)

with open(currentDir+'prtr_timing_'+pipeline_id+'.txt', 'w') as f:
    f.write(timing_string)
