# CourseQA Lesson 10

第10次课：让 CourseQA 更像真实项目。

## 功能

- FastAPI 查询接口
- TF-IDF 检索
- 历史记录保存到 `data/history.json`
- 查询历史、关键词搜索、时间筛选、删除和清空历史
- logging 日志保存到 `logs/courseqa.log`
- 文件读写异常处理

## 安装依赖

```bash
pip install fastapi uvicorn scikit-learn
```

## 启动服务

```bash
uvicorn app:app --reload
```

## 打开接口文档

浏览器访问：

```text
http://127.0.0.1:8000/docs
```

## 测试顺序

1. GET `/health`
2. POST `/query`
3. GET `/history`
4. GET `/history/search?keyword=FastAPI`
5. DELETE `/history/{record_id}`
6. DELETE `/history`
