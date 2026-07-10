# # 课程文件自动整理工具
## 功能说明
根据文件名关键字、文件后缀自动分类课程资料，满足作业全部约束：
1. 关键字`作业/练习/实验/任务`优先归入 `homework`
2. 无关键字时按后缀分 slides/code/data/documents/images/others
3. 默认复制文件，不删除原文件；支持move移动模式
4. 同名文件自动后缀加数字，不覆盖
5. --dry-run 预览模式，仅输出计划，无任何文件修改
6. 整理完成自动生成 `整理报告.txt`，包含全部统计明细
7. 加分扩展：--recursive 递归遍历子目录全部文件

## 目录分类规则
| 分类目录 | 匹配规则 |
|--------|--------|
| homework | 文件名含【作业/练习/实验/任务】（最高优先级） |
| slides | .ppt/.pptx/.key 课件 |
| code | .py/.ipynb/.c/.cpp/.java 代码文件 |
| data | .csv/.xlsx/.json 数据表格 |
| documents | .pdf/.doc/.docx/.txt/.md 文档 |
| images | .png/.jpg/.jpeg/.gif 图片 |
| others | 无法识别后缀的文件 |

## 运行命令示例
### 1. 预览dry-run模式（验收命令）
```bash
python main.py --source sample_materials --target organized_materials --dry-run