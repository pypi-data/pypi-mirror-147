import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

print('__main__')
print('__main__.__name__', __name__)
print('__main__.__package__', __package__)
print('sys.path', sys.path)

# https://www.jianshu.com/p/cb97d290c17f
# https://www.1024sou.com/article/207115.html

# 使用相对路径，那么执行 python funniestDemo就会出错
# from . import joke
from funniestDemo import joke
joke()