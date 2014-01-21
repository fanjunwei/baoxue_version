# coding=utf-8
from django.db import models

# Create your models here.

class Branch (models.Model):
    name = models.CharField(verbose_name='分支名',help_text='例如：F10_BXT_53', max_length=50,null=False,unique=True)
    createTime=models.DateTimeField(verbose_name='创建时间',null=False,auto_now_add=True)
    description=models.TextField(verbose_name='描述',default='')
    delFlag=models.BooleanField(verbose_name='删除标记',default=False,null=False)


class SubBranch (models.Model):
    name = models.CharField(verbose_name='子分支名',help_text='例如：8', max_length=50,null=False)
    branch=models.ForeignKey(Branch,null=False)
    fullName=models.CharField(verbose_name='子分支全名',max_length=50,null=False)
    createTime=models.DateTimeField(verbose_name='创建时间',null=False,auto_now_add=True)
    description=models.TextField(verbose_name='描述',default='')
    delFlag=models.BooleanField(verbose_name='删除标记',default=False,null=False)
    class Meta:
        unique_together=[('name','branch')]
    def save(self, force_insert=False, force_update=False, using=None):
        self.fullName='%s-%s'%(self.branch.name,self.name)
        models.Model.save(self,force_insert,force_update,using)

    def getFullName(self):
        return '%s-%s'%(self.branch.name,self.name)


class Version (models.Model):
    id=models.AutoField(verbose_name='id',primary_key=True)
    name = models.CharField(verbose_name='版本号',help_text='例如V01_2014-01-17_14_47', max_length=50,null=False,)
    fullName=models.CharField(verbose_name='子分支全名',max_length=50,null=False)
    subBranch=models.ForeignKey(SubBranch,null=False)
    createTime=models.DateTimeField(verbose_name='创建时间',null=False,auto_now_add=True)
    description=models.TextField(verbose_name='描述',default='')
    parent=models.IntegerField(verbose_name='基础版本',null=True)
    delFlag=models.BooleanField(verbose_name='删除标记',default=False,null=False)
    class Meta:
        unique_together=[('name','subBranch')]
    def getFullName(self):
        return '%s-%s_%s'%(self.subBranch.branch.name,self.subBranch.name,self.name)

    def save(self, force_insert=False, force_update=False, using=None):
        self.fullName='%s-%s_%s'%(self.subBranch.branch.name,self.subBranch.name,self.name)
        models.Model.save(self,force_insert,force_update,using)