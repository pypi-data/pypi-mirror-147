import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find('moha/')+len('moha/')]
print(curPath)
print(rootPath)
