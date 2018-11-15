# coding:utf8
from __future__ import unicode_literals
import xadmin
from xadmin import views

'''

'''


class clothing_salesman_registrationAdmin(object):
    search_box_flag = True
    list_display = ['name', 'the_month', 'staff_name', 'department', 'day01', 'day02', 'day03', 'day04', 'day05',
                    'day06', 'day07', "week1",
                    'day08', 'day09', 'day10', 'day11', 'day12', 'day13', 'day14', 'week2', 'day15', 'day16', 'day17',
                    'day18', 'day19', 'day20', 'day21', 'week3', 'day22', 'day23', 'day24', 'day25', 'day26', 'day27',
                    'day28', 'week4', 'day29', 'day30', 'day31', 'week5', 'month', 'create_time', 'update_time','complate','reson']

    search_fields = ['name', 'staff_name', 'department', 'the_month', 'create_time', 'update_time']

    list_filter = ['name', 'staff_name', 'department', 'the_month', 'create_time', 'update_time']
    list_editable = ['staff_name', 'day01', 'day02', 'day03', 'day04', 'day05', 'day06', 'day07',
                     'day08', 'day09', 'day10', 'day11', 'day12', 'day13', 'day14', 'day15', 'day16', 'day17',
                     'day18', 'day19', 'day20', 'day21', 'day22', 'day23', 'day24', 'day25', 'day26', 'day27',
                     'day28', 'day29', 'day30', 'day31','complate','reson' ]

    refresh_times = [False, 60]

    def get_list_queryset(self):
        request = self.request

        qs = super(clothing_salesman_registrationAdmin, self).get_list_queryset()


        name = request.GET.get('name', '')
        department = request.GET.get('department', '')
        staff_name = request.GET.get('staff_name', '')
        the_month=request.GET.get('the_month','')
        create_time= request.GET.get('create_time','')

        searchList = {

            'name__exact': name,
            'department__exact': department,
            'staff_name__exact': staff_name,
            'the_month__exact':the_month,
            'create_time__exact': create_time,
        }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        return qs





    # def month(self, instance):
    #     self.month=instance.week1+instance.week2+instance.week3+instance.week4+instance.week5
    #     return str(self.month)
    #     # self.month=instance.week1+instance.week2+instance.week3+instance.week4+instance.week5
    #
    # month.short_description = '月统计'
    # month.is_column = True
    # month.allow_tags = True
