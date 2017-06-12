用户API:
1. 获取所有用户信息
http://59.108.48.35:8080/api/user
2. 获取特定ID用户信息
http://59.108.48.35:8080/api/user/id/<int:id>
3. 获取特定组别用户信息
http://59.108.48.35:8080/api/user/group/<string:group>
4. 获取特定别名用户信息
http://59.108.48.35:8080/api/user/alias/<string:alias>

论文API:
1. 获取所有论文信息
http://59.108.48.35:8080/api/paper
2. 获取特定ID论文信息
http://59.108.48.35:8080/api/paper/id/<int:id>
3. 获取特定用户ID的所有论文信息
http://59.108.48.35:8080/api/paper/user_id/<int:id>

创建新用户API:
向http://59.108.48.35:8080/api/user的地址POST一个请求
其中, 请求实体中包含username和password, 请求头部中包含Basic认证(账号admin, 密码icstwip)
建议使用Chrome中的Poster插件实现


