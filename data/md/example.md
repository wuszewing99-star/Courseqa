Python overview: Python is widely used in web development, scripting, and data analysis.

Function basics: In Python, a function can accept a parameter and return a value. You define a function with def, pass a parameter into the function, and use return to send a value back.

Loop basics: A loop repeats actions. A for loop and a while loop are basic control structures.

JSONL notes: JSONL stores one JSON object per line. It is useful for saving structured text data.

Data structures: Lists and dictionaries are common Python data structures.

Python 是一种广泛使用的高级编程语言，以语法简洁和可读性高而闻名。Python 支持多种编程范式，包括面向对象、函数式和过程式编程。初学者可以直接使用 Python 进行变量赋值、运算和简单的控制流程操作，无需像其他编程语言那样提前声明变量类型。Python 的标准库丰富，提供了从文件操作、数据结构、网络编程到数据库操作的各类模块，使得学习者可以在短时间内快速构建实用程序，并且能够在不同领域的项目中进行应用，例如数据分析、Web 开发、自动化脚本和人工智能等。

Python 中的变量使用非常灵活，不需要事先声明类型，可以直接通过赋值操作生成。例如，将整数 10 赋值给变量 x，将字符串 "Alice" 赋值给变量 name。Python 提供了多种基本数据类型，包括整数、浮点数、布尔值、字符串、列表、元组、字典和集合等。每种数据类型都拥有丰富的方法和操作符，使得开发者可以轻松实现各种计算、逻辑判断和数据处理操作。此外，Python 对类型转换也提供了便捷的函数，例如 int()、str()、float() 等，使得数据处理更加灵活。

条件语句是 Python 的核心控制结构之一，用于根据条件执行不同的代码块。通过 if、elif 和 else 可以实现复杂的逻辑判断，例如根据用户年龄判断其是否为成年人。条件语句支持逻辑运算符和比较运算符的组合，使得开发者可以在程序中实现多条件判断和复杂业务逻辑处理。在实际项目中，条件语句常用于验证输入数据的合法性、分支执行不同的算法或流程以及处理异常场景，保证程序在各种情况下都能正确运行。

循环语句在 Python 中非常重要，常用于重复执行相同操作。Python 提供了 for 循环和 while 循环两种方式，可以遍历列表、字典、集合等可迭代对象。for 循环通常结合 range() 或可迭代对象使用，而 while 循环则根据条件执行，直到条件不满足为止。循环还支持 break 和 continue 控制语句，用于提前终止循环或跳过某次迭代。通过循环，程序可以自动化处理大量数据，提高开发效率，避免重复代码的编写。

列表是 Python 中最常用的数据结构之一，它是一个可变序列，支持动态添加、删除和修改元素。列表操作包括 append()、remove()、insert()、pop()、sort()、reverse() 等方法。通过切片操作，可以快速获取列表的子集，实现高效的数据处理。列表还支持嵌套，可以存储列表、字典或其他对象，方便实现复杂数据结构的管理。列表遍历和列表推导式是处理数据的常用技巧，能够在简洁代码的同时实现高效操作。

字典是 Python 中的键值对数据结构，使用方便且查询效率高。通过 key 可以快速访问对应的 value，支持动态增加、修改和删除元素。字典常用方法包括 get()、items()、keys()、values() 等。字典可以嵌套，用于存储复杂数据结构，例如学生成绩表、配置文件数据或 JSON 格式数据。通过字典的遍历和条件筛选，开发者可以高效地处理各类数据分析和业务逻辑场景。

函数是 Python 编程的基本单元，通过 def 关键字定义。函数可以接受参数、设置默认值、可变参数和关键字参数，同时支持返回值。函数的使用可以减少重复代码、提高程序可读性和可维护性。Python 还支持匿名函数 lambda，适合用于小型计算和回调操作。函数的调用顺序、作用域和参数传递机制是掌握 Python 编程的重要内容，良好的函数设计有助于构建模块化和可复用的程序。

模块化编程是 Python 的一大特点，开发者可以将相关函数、类和变量封装在独立文件中，使用 import 或 from ... import ... 语句导入模块。模块化有助于代码组织和复用，同时可以避免命名冲突。Python 官方提供了丰富的标准库模块，例如 math、datetime、os、json 等，开发者还可以使用 pip 安装第三方模块，例如 requests、pandas、numpy，用于网络请求和数据分析任务。

文件操作是 Python 常用技能，涵盖文本文件和二进制文件的读写。使用 open()、read()、write() 和 with 上下文管理器，可以安全、方便地处理文件。对于 JSON、CSV 等格式的文件，Python 提供了专门的模块，例如 json、csv，可以高效地进行序列化和反序列化操作。文件操作技能在数据分析、日志处理和配置管理中应用广泛，是 Python 编程基础之一。

异常处理在 Python 中通过 try...except...finally 实现，用于捕获和处理运行时错误，保证程序的稳定性。通过异常处理，可以优雅地处理用户输入错误、文件操作错误或网络请求失败等情况，同时记录日志便于排查问题。finally 子句保证无论异常是否发生，必要的清理操作都能执行，例如关闭文件或数据库连接。合理使用异常处理可以显著提升程序健壮性。

列表推导式是 Python 高效生成列表、集合或字典的一种语法糖。例如 [x**2 for x in range(10)] 可以快速生成平方列表。推导式可加条件过滤元素，例如 [x for x in range(10) if x % 2 == 0]。推导式语法简洁，代码量少，可读性高，是 Python 开发者处理数据集合时常用技巧之一。通过嵌套推导式，还可以生成多维列表，实现复杂数据结构的构建。

面向对象是 Python 的核心概念之一，使用 class 定义类，可以创建对象并赋予属性和方法。支持继承、多态和封装，方便开发者构建大型程序。Python 的类还可以定义特殊方法（如 __init__、__str__、__repr__）来控制对象初始化和打印输出。掌握面向对象编程有助于设计可维护、可扩展的软件系统。

装饰器是 Python 的高级功能，可以在不修改函数源代码的情况下增强函数功能。通过 @装饰器语法，可以轻松实现日志记录、权限校验、性能监控等功能。装饰器本质是函数返回函数，理解闭包机制对装饰器的设计和使用非常重要。合理使用装饰器可以提升代码复用性和可维护性。

生成器使用 yield 关键字逐步生成序列，而不是一次性生成所有元素，从而节省内存。生成器可以在 for 循环中迭代使用，也可以与 next() 配合使用。生成器在处理大数据或无限序列时非常有用，例如处理日志文件或网络数据流。掌握生成器可以提升 Python 程序的性能和内存效率。

FastAPI 是一个现代 Python Web 框架，支持异步编程和自动生成 Swagger UI 文档。通过 FastAPI，可以快速构建 API 服务，定义 GET、POST 等请求接口，并自动校验参数类型。FastAPI 还支持依赖注入、中间件和 WebSocket，适合构建高性能、可维护的后端服务。在课堂项目中，FastAPI 可以将离线检索功能封装成接口，便于前端调用。

GET 请求用于从服务器获取资源，参数一般放在 URL 中。POST 请求用于提交数据，参数通常放在 JSON 请求体中。FastAPI 会自动根据函数注解验证参数类型，并返回 JSON 响应。理解 GET 与 POST 的区别，对于设计 RESTful 接口至关重要。

路由定义是 FastAPI 的核心操作，通过 @app.get() 或 @app.post() 装饰器指定 URL 和处理函数。例如 @app.get("/query") 定义查询接口。每个路由对应一个处理函数，接收请求参数并返回响应。通过路由设计，可以清晰组织接口功能，提高 API 可维护性。


