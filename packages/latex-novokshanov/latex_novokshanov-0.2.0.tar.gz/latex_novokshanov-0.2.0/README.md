# Домашнее задание 1


## Задание 1

Были написаны 2 скрипта Python: `latex_generation.py`, `latex_example.py`

Для формирования файла latex необходимо запустить `latex_example.py` из директории `hw_2`.

```
python3 latex_example.py
```

Выходной файл `example_table.tex` лежит в директории `artifacts`.


## Задание 2

```bash
(venv) novokshanov-e@i109893575:~/ITMO/ITMO-python/hw_2$ 
     python setup.py sdist bdist_wheel
     
running sdist
running egg_info
creating latex_gen_novokshanov.egg-info
writing latex_gen_novokshanov.egg-info/PKG-INFO
writing dependency_links to latex_gen_novokshanov.egg-info/dependency_links.txt
writing top-level names to latex_gen_novokshanov.egg-info/top_level.txt
writing manifest file 'latex_gen_novokshanov.egg-info/SOURCES.txt'
reading manifest file 'latex_gen_novokshanov.egg-info/SOURCES.txt'
writing manifest file 'latex_gen_novokshanov.egg-info/SOURCES.txt'
running check
warning: check: missing required meta-data: url

creating latex-gen-novokshanov-0.1.0
creating latex-gen-novokshanov-0.1.0/latex_gen_novokshanov.egg-info
copying files to latex-gen-novokshanov-0.1.0...
copying README.md -> latex-gen-novokshanov-0.1.0
copying setup.py -> latex-gen-novokshanov-0.1.0
copying latex_gen_novokshanov.egg-info/PKG-INFO -> latex-gen-novokshanov-0.1.0/latex_gen_novokshanov.egg-info
copying latex_gen_novokshanov.egg-info/SOURCES.txt -> latex-gen-novokshanov-0.1.0/latex_gen_novokshanov.egg-info
copying latex_gen_novokshanov.egg-info/dependency_links.txt -> latex-gen-novokshanov-0.1.0/latex_gen_novokshanov.egg-info
copying latex_gen_novokshanov.egg-info/top_level.txt -> latex-gen-novokshanov-0.1.0/latex_gen_novokshanov.egg-info
Writing latex-gen-novokshanov-0.1.0/setup.cfg
creating dist
Creating tar archive
removing 'latex-gen-novokshanov-0.1.0' (and everything under it)
running bdist_wheel
running build
/home/novokshanov-e/ITMO/ITMO-python/hw_2/venv/lib/python3.10/site-packages/setuptools/command/install.py:34: SetuptoolsDeprecationWarning: setup.py install is deprecated. Use build and pip and other standards-based tools.
  warnings.warn(
installing to build/bdist.linux-x86_64/wheel
running install
running install_egg_info
Copying latex_gen_novokshanov.egg-info to build/bdist.linux-x86_64/wheel/latex_gen_novokshanov-0.1.0.egg-info
running install_scripts
creating build/bdist.linux-x86_64/wheel/latex_gen_novokshanov-0.1.0.dist-info/WHEEL
creating 'dist/latex_gen_novokshanov-0.1.0-py3-none-any.whl' and adding 'build/bdist.linux-x86_64/wheel' to it
adding 'latex_gen_novokshanov-0.1.0.dist-info/METADATA'
adding 'latex_gen_novokshanov-0.1.0.dist-info/WHEEL'
adding 'latex_gen_novokshanov-0.1.0.dist-info/top_level.txt'
adding 'latex_gen_novokshanov-0.1.0.dist-info/RECORD'
removing build/bdist.linux-x86_64/wheel
(venv) novokshanov-e@i109893575:~/ITMO/ITMO-python/hw_2$ 
     twine upload dist/*
     
Uploading distributions to https://upload.pypi.org/legacy/
Uploading latex_gen_novokshanov-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.9/3.9 kB • 00:00 • ?
Uploading latex-gen-novokshanov-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.9/3.9 kB • 00:00 • ?

View at:
https://pypi.org/project/latex-gen-novokshanov/0.1.0/
(venv) novokshanov-e@i109893575:~/ITMO/ITMO-python/hw_2$ pip install latex-gen-novokshanov
Collecting latex-gen-novokshanov
  Downloading latex_gen_novokshanov-0.1.0-py3-none-any.whl (1.2 kB)
Installing collected packages: latex-gen-novokshanov
Successfully installed latex-gen-novokshanov-0.1.0
(venv) novokshanov-e@i109893575:~/ITMO/ITMO-python/hw_2$ 
```

Как видим, пакет успешно опубдикован и успешно установлен в локальном окружении.

https://pypi.org/project/latex-gen-novokshanov/0.1.0/#description

