# coding=utf-8


from django.db import models
from skuapp.table.public import *


CLOTHING = (
    ('FZ', u'服装'),
    ('FFZ', u'非服装')
)


class t_product_quality_feedback(models.Model):
    SubmitTime          =   models.DateTimeField(u'提交日期', blank=True, null=True)
    Submitter           =   models.CharField(u'提交人', max_length=32, blank=True, null=True)
    SKU                 =   models.CharField(u'SKU', max_length=64, null=True)
    Plateform           =   models.CharField(u'平台', max_length=32, choices=getChoices(ChoiceQualityFeedbackPlateform), null=True)
    OrderID             =   models.CharField(u'普源订单号', max_length=32, blank=True, null=True)
    ProblemType         =   models.CharField(u'问题类型', max_length=32, choices=getChoices(ChoiceQualityFeedbackType), null=True)
    Detail              =   models.TextField(u'具体反馈', null=True)
    Picture_1           =   models.FileField(u'图片一(选填)', blank=True, null=True)
    Picture_2           =   models.FileField(u'图片二(选填)', blank=True, null=True)
    Picture_3           =   models.FileField(u'图片三(选填)', blank=True, null=True)
    Picture_4           =   models.FileField(u'图片四(选填)', blank=True, null=True)
    Picture_5           =   models.FileField(u'图片五(选填)', blank=True, null=True)
    CPZY                =   models.CharField(u'产品专员', max_length=32, blank=True, null=True)
    CPZY_Note           =   models.TextField(u'产品专员备注', blank=True, null=True)
    CGY                 =   models.CharField(u'采购员', max_length=32, blank=True, null=True)
    CGY_Note            =   models.TextField(u'采购员备注', blank=True, null=True)
    ZJY                 =   models.CharField(u'质检员', max_length=32, blank=True, null=True)
    ZJY_Note            =   models.TextField(u'质检员备注', blank=True, null=True)
    CKY                 =   models.CharField(u'仓库员', max_length=32, blank=True, null=True)
    CK_Note             =   models.TextField(u'仓库备注', blank=True, null=True)
    ZJY_Final           =   models.CharField(u'最终审核人', max_length=32, blank=True, null=True)
    Final_Note          =   models.TextField(u'最终备注', blank=True, null=True)
    Reject_Reason       =   models.TextField(u'驳回原因', blank=True, null=True)
    Step                =   models.TextField(u'进度', blank=True, null=True)
    Source_Origin       =   models.CharField(u'最初来源页面', max_length=32, blank=True, null=True)
    Source_ID           =   models.IntegerField(u'最初来源ID', max_length=11, blank=True, null=True)
    Last_ID             =   models.IntegerField(u'上一步来源ID', max_length=11, blank=True, null=True)
    State               =   models.CharField(u'状态', max_length=10, choices=getChoices(ChoiceQualityFeedbackState), blank=True, null=True)
    ClothingFlag        =   models.CharField(u'是否服装', max_length=5, choices=CLOTHING, null=True)

    class Meta:
        app_label = 'skuapp'
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.id)