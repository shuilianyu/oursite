from django.db import models

# Create your models here.
class Jobs(models.Model):
    job_title = models.CharField('工作职位',max_length=20,null=True,blank=True)
    job_categories = models.CharField('职位性质',max_length=20,null=True,blank=True)
    wage1 = models.IntegerField('最低工资',null=True,blank=True)
    wage2 = models.IntegerField('最高工资',null=True,blank=True)
    location = models.CharField('地址',max_length=25,null=True,blank=True)
    work_experience = models.CharField('工作经验',max_length=10,null=True,blank=True)
    education = models.CharField('学历',max_length=10,null=True,blank=True)
    recruits_number = models.CharField('招聘人数',max_length=10,null=True,blank=True)
    company_name = models.CharField('公司名字',max_length=20,null=True,blank=True)
    company_type = models.CharField('公司类型',max_length=10,null=True,blank=True)
    company_size = models.CharField('公司规模',max_length=10,null=True,blank=True)
    company_address = models.CharField('公司详细地址',max_length=16,null=True,blank=True)
    welfare_pos = models.CharField('各种福利',max_length=100,null=True,blank=True)
    job_description = models.TextField('工作详情',null=True,blank=True)

    def __str__(self):
        return self.job_title