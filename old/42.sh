#!/usr/bin sh
#
# 串联训练流程，连续训练出60天结果
#

days=(20150601 20150602 20150603 20150604 20150605 20150606 20150607 20150608
      20150609 20150610
      20150611 20150612 20150613 20150614 20150615 20150616 20150617 20150618
      20150619 20150620
      20150621 20150622 20150623 20150624 20150625 20150626 20150627 20150628
      20150629 20150630
      20150901 20150702 20150703 20150704 20150705 20150706 20150707 20150708
      20150709 20150710
      20150711 20150712 20150713 20150714 20150715 20150716 20150717 20150718
      20150719 20150720
      20150721 20150722 20150723 20150724 20150725 20150726 20150727 20150728
      20150729 20150730 20150731
      20150801 20150802 20150803 20150804 20150805 20150806 20150807 20150808
      20150809 20150810
      20150811 20150812 20150813 20150814 20150815 20150816 20150817 20150818
      20150819 20150820
      20150821 20150822 20150823 20150824 20150825 20150826 20150827 20150828
      20150829 20150830 20150831
      20150901 20150902 20150903 20150904 20150905 20150906 20150907 20150908
      20150909 20150910
      20150911 20150912 20150913 20150914 20150915 20150916 20150917 20150918
      20150919 20150920
      20150921 20150922 20150923 20150924 20150925 20150926 20150927 20150928
      20150929 20150930
      20151001 20151002 20151003 20151004 20151005 20151006 20151007 20151008
      20151009 20151010
      20151011 20151012 20151013 20151014 20151015 20151016 20151017 20151018
      20151019 20151020
      20151021 20151022 20151023 20151024 20151025 20151026 20151027 20151028
      20151029 20151030)

train_day=91
predict_day=92
b1_day=91
b7_day=85
b30_day=63
b90_day=3

#python make_train_feats.py 20150831 20150830 20150824 20150802 20150602
#python make_label.py 20150830 20150801
#python train.py 20150830 20150831

# 训练10天
for (( i = 0; i < 60; i++ )); do
    echo ${days[`expr ${train_day} + $i`]}
    echo 'Make Feats and Label'
    python make_train_feats.py ${days[`expr ${predict_day} + $i`]} ${days[`expr ${b1_day} + $i`]} ${days[`expr ${b7_day} + $i`]} ${days[`expr ${b30_day} + $i`]} ${days[`expr ${b90_day} + $i`]}
    python make_label.py ${days[`expr ${train_day} + $i`]} ${days[`expr ${b30_day} + $i - 1`]}

    echo 'Training...'
    python train.py ${days[`expr ${train_day} + $i`]} ${days[`expr ${predict_day} + $i`]}
    echo "Reducing..."
    python result_and_train_set.py ${days[`expr ${predict_day} + $i`]}
    python submit.py ${days[`expr ${predict_day} + $i`]}

    echo 'Done'

done


echo 'OK, Done'
