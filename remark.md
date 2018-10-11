项目说明
1.本项目用于分析针对python相关职位的信息展示，特点在于数据视图展示

项目参考
    1.百度首页搜索，跳转到下一页显示，并模拟点击实现ajax加载
    2.智联招聘的翻页按钮格式，以及页面布局
    
项目使用
    1.直接python manage.py runserver运行
    
注意：
    本项目中连接的mongodb数据库为服务器上的mongodb数据库
    可以通过运行mongodb.py文件，使在本地的mongodb中产生两个集合(运行时间很长，大约需要30分钟)
    1. db：zhilianzhaopin collection：jobs
    2. db：zhilianzhaopin collection：classify
    进而修改 zhilianzhaopin/view.py 中JobMesView类初始化对应的mongodb host
    连接本机数据库
    

在本项目中存在以下尚待完善功能
    1.没有关键词提示功能
    2.页面美观程度
    3.页面适用于google浏览器,其他浏览器暂无测试
    *.各种数据视图为没有与数据库连接(由于服务器运行内存较低),缺乏实时性,可直接调用相应的类方法使其动态生成
    
项目展示
    http://www.yangfubo.xyz