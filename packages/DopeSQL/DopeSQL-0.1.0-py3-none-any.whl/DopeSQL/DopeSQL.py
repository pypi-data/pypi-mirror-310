# 目前支持的功能简单，之后慢慢加。

# 计划加上语法限制--->  

# - 整理出通过 FROM 声明的表名，未声明的表名禁止在后面使用

# - 整理出通过 SELECT 声明的列名，未声明的列名禁止在后面使用

# - 规定必须按照逻辑顺序书写语句，判断关键字是否按逻辑顺序书写，不按逻辑顺序书写时报错。

import re

# 注意事项（原生SQL知识）
# - 隐式连接（FROM T1, T2 WHERE T1.c = T2.cc）  等同于 INNER JOIN 连接。
# - 在不使用等号进行表连接的情况下，直接 FROM 多个表并 SELECT 多个表中的数据，会进行笛卡尔积查询。
# - 连表查询时如果遇到对多个同名列的访问就会报错，除非用 AS 语句将这些同名列重命名来消除重名。（简单说，包含同名列的查询必定失败，除非重命名）


def python_to_sql(python_expr):
    # 将 Python 表达式转换为 SQL 语句的简单实现
    # 只支持 SELECT 语句和 WHERE 条件中的简单比较操作

    # 初始化 SELECT 和 FROM 部分
    select_part = "SELECT "
    from_part = "FROM "
    where_part = ""

    # 检查是否包含 WHERE 子句
    if 'if' in python_expr:

        # 提取循环变量名
        var_loop = re.search(r'\bfor\s+(\w+)\s+in\b', python_expr).group(1)
        
        # 提取条件部分
        # 截取 "if" 之后的字符串
        condition = python_expr.split('if')[1].strip()
        # 删除末尾的"]"
        condition = condition[:condition.rfind(']')]
        
        # 构建WHERE子句
        where_part = " WHERE " + condition.replace(f'{var_loop}[\'' , '')\
                    .replace('\']', '').replace('>', '>')\
                    .replace('>=', '>=').replace('<', '<')\
                    .replace('<=', '<=').replace('==', '=')\
                    .replace('and', 'AND')
        where_part = where_part.strip()

    # 提取选择的列
    pattern = r'\{([^}]*)\}'
    match = re.search(pattern, python_expr).group(1)
    pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\"*\'*\s*\:\s*'
    col_list = re.findall(pattern, match)
    cols = ', '.join(col_list)

    # 提取目标数据表
    pattern = r"in\s+([^ ]+)(?=\s+if|\])"
    table_name = re.search(pattern, python_expr).group(1)

    # 拼接完整的 SQL 语句
    sql_statement = select_part + cols + " " + from_part + table_name + " " + where_part

    return sql_statement

def dopeSQL(sql, debug=False):
    """编译易读SQL为可执行SQL语句。"""

    def _extract_aggtarget(s):
        """提取聚合函数括号内的字段名。"""
        # 定义关键词列表
        keywords = ['MAX', 'MIN', 'AVG', 'SUM', 'COUNT']
        # 编译一个正则表达式，用于匹配括号内的内容
        pattern = re.compile(r'(\b(?:MAX|MIN|AVG|SUM|COUNT)\b)\s*\((.*?)\)')

        # 查找所有匹配项
        matches = pattern.findall(s)

        # 提取括号内的内容
        results = [match[1] for match in matches]

        return results

    def _remove_element(text, target):
        """移除序列中的字段名及其前面的第一个逗号"""
        # 构建正则表达式，匹配目标字符串及其前面的逗号和空白字符
        pattern = r',\s*' + re.escape(target)
        
        # 使用 re.sub 替换匹配到的内容为空字符串
        result = re.sub(pattern, '', text)
        
        return result

    # 分割SQL语句
    parts = sql.split('\n')

    # 创建字典来保存各部分的顺序
    sql_parts = {
        'FROM': [],
        'SELECT': [],
        'WHERE': [],
        'JOIN': [],
        'GROUP BY': [],
        'AGG...': [],
        'HAVING': [],
    }

    aggs = ['MAX(', 'MIN(', 'AVG', 'SUM(', 'COUNT(']

    cols_agged = []
    

    # 遍历分割后的部分，将它们分类
    for part in parts:
        if 'FROM' in part.upper():                                              # 注意当没有使用JOIN功能时，不需要从 FROM 行中剔除多余的表，因为通过 FROM 指定多余的表并不会导致报错。
            sql_parts['FROM'].append(part.strip())
            
        elif 'SELECT' in part.upper():
            sql_parts['SELECT'].append(part.strip())

        elif 'JOIN' in part.upper():                                            # 注意连接聚合复合语句，逻辑上是先连接再聚合的。
            line_join = part.strip()
            
            # 获得被连接的列名 & 表名
            cols_joined   = line_join.split("JOIN")[1].split(",")               # 尚未剔除列名字符串左右空格
            tables_joined = [col.split(".")[0].strip() for col in cols_joined]

            # 从最终的 FROM 语法行中移除可执行 SQL 不需要的表名
            for table in tables_joined:
                sql_parts["FROM"][0] = _remove_element(sql_parts["FROM"][0], table)

            # 生成最终 JOIN 语句
            for i in range(1, len(tables_joined)):
                code = line_join.split("JOIN")[0] + "JOIN " + \
                        tables_joined[i] + " ON " + \
                        cols_joined[i-1].strip() + " = " + cols_joined[i].strip()
                        
                sql_parts['JOIN'].append(code)
            
        elif 'WHERE' in part.upper():
            sql_parts['WHERE'].append(part.strip())
            
        elif 'GROUP BY' in part.upper():
            sql_parts['GROUP BY'].append(part.strip())
            
        elif any(agg in part.upper() for agg in aggs):
            sql_parts['AGG...'].append(part.strip())

            # 获得被聚合的字段名
            cols_agged = cols_agged + _extract_aggtarget(part)

            # 从最终的 SELECT 语法行中移除对应的字段
            for col in cols_agged:
                sql_parts["SELECT"][0] = _remove_element(sql_parts["SELECT"][0], col)
            
        elif 'HAVING' in part.upper():
            sql_parts['HAVING'].append(part.strip())
        
    # 按照SELECT, FROM, WHERE的顺序重组SQL语句
    ordered_sql = '\n'.join(sql_parts['SELECT'])
    ordered_sql += ', ' + ', '.join(sql_parts['AGG...']) + '\n' if sql_parts['AGG...'] else '\n'
    ordered_sql += '\n'.join(sql_parts['FROM']) + '\n' + \
                    ('\n'.join(sql_parts['JOIN']) + '\n' if sql_parts['JOIN'] else "") + \
                    '\n'.join(sql_parts['WHERE']) + '\n' + \
                    '\n'.join(sql_parts['GROUP BY']) + '\n' + \
                    '\n'.join(sql_parts['HAVING']) + '\n'

    if debug == True:
        print("编译后的SQL（前500个字符）: ", ordered_sql.strip()[:500])

    return ordered_sql.strip()


if __name__ == "__main__":
    # 示例 Python 表达式
    python_expr_without_where = """
    results = [{ 'col1': row['col1'], 'col2': row['col2'] } for row in db.table]
    """
     
    python_expr_with_where = """
    results = [
       {'col1': row['col1'], 'col2': row['col2']}
       for row in db.table if row['col2'] > 100 and row['col1'] == 'hello'
    ]
    """
     
    # 转换为 SQL
    sql_without_where = python_to_sql(python_expr_without_where)
    sql_with_where = python_to_sql(python_expr_with_where)

    print("SQL 带WHERE:")
    print(sql_without_where)
    print("\nSQL 不带WHERE:")
    print(sql_with_where)
    print("\n\n")
    print("==================================================\n")


    # 示例易读SQL语句
    sql_input = '''
        FROM table_a AS a, table_b AS b
        SELECT a.col_1, a.col_2, b.col_3
        WHERE a.col_1 = b.col_2 AND a.col_3 <= 5
    '''

    sql_input_2 = '''
        FROM table_a
        SELECT col_1, col_2, col_3
        WHERE col_1 > 1
        GROUP BY col_1
            SUM(col_2) AS sum_2
            AVG(col_3) AS avg_3
        HAVING sum_2 > 10
    '''

    sql_input_3 = '''
        FROM table
        SELECT c1, c2
        WHERE c3 > 30
    '''

    sql_input_4 = '''
        FROM table_1, table_2, table_3
        SELECT *
        INNER JOIN table_1.col_1, table_2.col_2, table_3.col_3
        WHERE table_3.col_3 > 30
    '''

    # 转换并打印可执行的SQL语句
    print(dopeSQL(sql_input))
    print("\n")

    # 转换并打印可执行的SQL语句
    print(dopeSQL(sql_input_2))
    print("\n")

    print(dopeSQL(sql_input_3))
    print("\n")

    print(dopeSQL(sql_input_4))

    






    
