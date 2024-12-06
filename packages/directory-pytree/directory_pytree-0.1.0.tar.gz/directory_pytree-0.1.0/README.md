```markdown
# PyTree

一个简单而强大的目录树显示工具。

## 安装

‍‍```bash
pip install directory-pytree
```

## 使用方法

```bash
pytree [路径] [-e 排除目录] [-L 层级] [-s]
```

### 参数说明

- 路径: 要显示的目录路径（可选，默认为当前目录）
- -e, --exclude: 要排除的目录列表
- -L, --level: 最大显示深度
- -s, --size: 显示文件大小

### 示例

```bash
pytree
pytree /path/to/directory
pytree -s -L 2
pytree -e node_modules .git
```

## 开发

1. 克隆仓库
2. 安装开发依赖: pip install -e ".[dev]"
3. 运行测试: pytest

## 许可证

MIT License
Copyright (c) 2023 Chen Ding Gang