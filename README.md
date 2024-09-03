## 开发

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 添加统一日志记录
```

## 部署

```
docker build --platform linux/amd64  . --file Dockerfile --tag registry.cn-beijing.aliyuncs.com/biyao/spider:myinterface-v1
echo "416798gao" | docker login registry.cn-beijing.aliyuncs.com -u sdgaozhe@qq.com --password-stdin
docker push registry.cn-beijing.aliyuncs.com/biyao/spider:myinterface-v1
```