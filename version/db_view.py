# coding=utf-8
from django.db import models
'''
create view v_browse as select `version_version`.`id` AS `id`,`version_version`.`name` AS `version_name`,`version_subbranch`.`name` AS `subbranch_name`,`version_branch`.`name` AS `branch_name`,`version_version`.`fullName` AS `fullName`,`version_version`.`createTime` AS `version_createTime`,`version_version`.`description` AS `description`,`version_version`.`parent` AS `parent`,`version_version`.`parentFullName` AS `parentFullName`,`version_subbranch`.`description` AS `subbranch_description`,`version_branch`.`description` AS `branch_description` from ((`version_version` join `version_subbranch` on((`version_version`.`subBranch_id` = `version_subbranch`.`id`))) join `version_branch` on((`version_subbranch`.`branch_id` = `version_branch`.`id`))) order by `version_branch`.`name`,`version_subbranch`.`name`,`version_version`.`createTime`;
'''



class VBrows (models.Model):
    id=models.AutoField(verbose_name='id',primary_key=True)
    version_name = models.CharField(verbose_name='版本号',help_text='例如V01_2014-01-17_14_47', max_length=50,null=False,)
    subbranch_name = models.CharField(verbose_name='子分支名', max_length=50,null=False,)
    branch_name = models.CharField(verbose_name='分支名', max_length=50,null=False,)
    fullName=models.CharField(verbose_name='版本全名',max_length=50,null=False)
    version_createTime=models.DateTimeField(verbose_name='创建时间',null=False)
    description=models.TextField(verbose_name='版本描述',default='')
    subbranch_description=models.TextField(verbose_name='子分支描述',default='')
    branch_description=models.TextField(verbose_name='分支描述',default='')
    parent=models.IntegerField(verbose_name='基础版本ID',null=True)
    parentFullName=models.CharField(verbose_name='基础版本全名',max_length=50,null=True)
    version_username=models.CharField(max_length=30,verbose_name='提交用户名',null=True)
    class Meta:
        db_table='v_browse'


