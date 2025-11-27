# 待办系统 (Todo System)

一个使用 FastAPI + Tortoise-ORM + Jinja2 开发的现代化网页待办系统。

## 技术栈

- **后端框架**: FastAPI - 高性能 Python Web 框架
- **ORM**: Tortoise-ORM - 异步 ORM 框架
- **模板引擎**: Jinja2 - 强大的模板渲染引擎
- **数据库**: SQLite - 轻量级关系型数据库
- **密码加密**: bcrypt - 安全的密码哈希算法
- **身份验证**: JWT - JSON Web Token
- **依赖管理**: uv - 快速的 Python 包管理器

## 功能特性

### 用户模块
- ✅ 用户注册（用户名3-20位，密码6-16位）
- ✅ 用户登录（JWT身份验证）
- ✅ 用户退出（清除登录状态）
- ✅ 密码加密存储
- ✅ 用户名唯一性校验

### 待办模块
- ✅ 添加待办事项（标题必填，内容可选）
- ✅ 编辑待办事项
- ✅ 删除待办事项
- ✅ 标记待办事项为完成/未完成
- ✅ 待办事项按创建时间倒序显示
- ✅ 分未完成/已完成列表展示
- ✅ 仅显示当前用户的待办事项

### 页面与交互
- ✅ 极简现代化UI设计
- ✅ 响应式布局，支持移动端
- ✅ 表单提交禁用按钮防重复提交
- ✅ 操作成功/失败提示消息
- ✅ 已完成待办事项显示删除线
- ✅ 编辑功能使用模态框

## 项目结构

```
.
├── main.py                 # 主应用文件
├── models/                # 数据模型
│   ├── user.py           # 用户模型
│   └── todo.py           # 待办模型
├── routes/               # 路由模块
│   ├── auth.py           # 认证路由（注册、登录、退出）
│   └── todo.py           # 待办路由（增删改查）
├── templates/            # Jinja2模板
│   ├── auth/             # 认证页面
│   │   ├── login.html    # 登录页面
│   │   └── register.html # 注册页面
│   └── todo/             # 待办页面
│       └── index.html    # 主页
├── static/               # 静态资源
│   └── css/              # 样式文件
│       └── style.css     # 主样式
├── pyproject.toml        # 项目配置
├── uv.lock               # 依赖锁定文件
└── README.md             # 项目文档
```

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 启动应用

```bash
uv run python main.py
```

或使用 uvicorn 直接启动：

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问应用

打开浏览器访问：http://localhost:8000

## API 文档

### 健康检查

```
GET /health
```

响应：
```json
{
  "status": "healthy"
}
```

### 认证接口

#### 用户注册
```
GET /auth/register          # 注册页面
POST /auth/register         # 注册提交
```

#### 用户登录
```
GET /auth/login            # 登录页面
POST /auth/login           # 登录提交
```

#### 用户退出
```
POST /auth/logout          # 退出登录
```

### 待办接口

#### 主页（待办列表）
```
GET /                      # 显示待办列表
```

#### 添加待办
```
POST /add                  # 添加新待办
```

#### 编辑待办
```
POST /edit/{todo_id}       # 编辑待办
```

#### 标记完成/未完成
```
POST /toggle/{todo_id}     # 切换待办状态
```

#### 删除待办
```
POST /delete/{todo_id}     # 删除待办
```

## 数据库

项目使用 SQLite 数据库，数据库文件会自动创建在项目根目录下的 `todo.db`。

## 配置说明

### JWT 配置

在 `routes/auth.py` 中：
- `SECRET_KEY`: JWT 密钥，生产环境中请修改为随机字符串
- `ALGORITHM`: 加密算法，默认使用 HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token 过期时间，默认 30 分钟

### 数据库配置

在 `main.py` 中：
- `db_url`: 数据库连接 URL，默认使用 SQLite
- `modules`: 模型模块配置
- `generate_schemas`: 是否自动生成数据库表，默认开启

## 开发说明

### 代码规范
- 使用异步编程（async/await）
- 路由和 ORM 操作全异步
- 关键逻辑添加注释
- 捕获异常并返回友好提示

### 热重载

开发模式下已启用热重载，修改代码后会自动重启服务器。

## 部署

### 生产环境建议
1. 修改 `SECRET_KEY` 为随机字符串
2. 关闭 `generate_schemas`（首次部署后）
3. 使用更安全的数据库（如 PostgreSQL）
4. 配置 HTTPS
5. 使用进程管理器（如 Gunicorn）

## 许可证

MIT License