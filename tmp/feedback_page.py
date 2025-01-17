import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

import datetime as pydatetime
import pandas as pd
from itertools import zip_longest
import numpy as np

# from PIL import Image
form_2nd_cls = uic.loadUiType("ui/feedback_widget2.ui")[0]

class SecondWindowCls(QDialog, QWidget, form_2nd_cls):
    def __init__(self, mainInfoDict):
        super(SecondWindowCls, self).__init__()
        self.initUi(mainInfoDict)
        # self.initUi()
        # self.show()

        # 선택지
        self.tePrevBtn.clicked.connect(self.tePrevBtn_clicked)
        self.teNextBtn.clicked.connect(self.teNextBtn_clicked)

    def initUi(self, mainInfo):
    # def initUi(self):
        self.setupUi(self)

        self.infoDict = mainInfo
        self.testCnt = 1
        self.teStartTs = self.get_now_timestamp()
        self.corrList = []
        self.inCorrList = []

        self.df2 = pd.DataFrame([['FDB'+str(self.testCnt)+'_START', self.teStartTs]],
                               index=[self.infoDict['idxCnt']], columns=['status', 'ts'])
        self.infoDict['idxCnt'] += 1
        self.df2.to_csv(self.infoDict['fileName'], mode='a', header=False, index=False)

        # self.nameLabel2.setText(self.infoDict['name'])
        # self.expCntLabel2.setText(self.infoDict['expCnt'])
        # self.expTypeLabel2.setText("Post-TEST")

        # 문제풀이 결과, AoI 정보 업데이트하는 함수 추가 (엑셀 읽어서 데이터 받아오기)
        result_fPath = 'output/test/post/'
        self.get_test_result(result_fPath)

        self.imgFullPath = 'imgs/resizing2/' + self.infoDict['expCnt'] + '/'
        self.imgList = os.listdir(self.imgFullPath)
        self.imgList.sort()

        self.teAns = 0

        self.imgIdx = 0
        self.imgIdx = self.testCnt * 2 - 2

        # questPixmap = QPixmap("imgs/questions/" + str(self.testCnt) + "_resizing.jpg")
        questPixmap = QPixmap(self.imgFullPath + self.imgList[self.imgIdx])
        self.teLabel.setPixmap(questPixmap)
        self.teLabel.resize(questPixmap.width(), questPixmap.height())


    def tePrevBtn_clicked(self):
        print("in prev")

    def teNextBtn_clicked(self):
        print("in next")

    def updateTest(self):
        print("in updateTest")


    # def teSubmitBtn_cicked(self):
    #     # QMessageBox.about(self, '선택정답', str(self.teAns)+'번')
    #     if self.teAns == 0:
    #         QMessageBox.information(self, 'error!', '정답을 선택하세요!')
    #
    #     else:
    #         self.teEndTs = self.get_now_timestamp()
    #
    #         # self.df2.append({'status':'TE'+str(self.testCnt)+'_END', 'ts':self.teEndTs, 'ans':self.teAns, 'confidence':-1}, ignore_index=True)
    #         self.df3 = pd.DataFrame([['TE'+str(self.testCnt)+'_END&CONF'+str(self.testCnt)+'_START', self.teEndTs, self.teAns, -1, ans_res]],
    #                                 index=[self.infoDict['idxCnt']], columns=['status', 'ts', 'ans', 'confidence', 'res'])
    #         self.infoDict['idxCnt'] += 1
    #         # self.df3.to_csv(self.infoDict['fileName'], mode='a', header=False, index=True)
    #         self.df3.to_csv(self.infoDict['fileName'], mode='a', header=False, index=False)
    #
    #         self.hide()
    #         self.confidence_page = ThirdWindowCls(self.infoDict, self.testCnt, self)
    #         # self.third = ThirdWindowCls(self.infoDict, self.testCnt)
    #         # self.third.exec()
    #         # self.show()
    #
    #
    #         if self.testCnt < 6:
    #             self.testCnt += 1
    #             # self.updateUI()
    #             self.confidence_page.show()
    #         else:
    #             self.close()


    def get_now(self):
        # 현재 시스템 시간을 datetime형으로 반환
        return pydatetime.datetime.now()

    def get_now_timestamp(self):
        # 현재 시스템 시간을 POSIX timestamp float형으로 반환
        return self.get_now().timestamp()

    def get_test_result(self, fPath):
        resFileList = os.listdir(fPath)
        resFileList.sort(reverse=True)
        resFile = ''

        for resF in resFileList:
            validChkStr = resF.split('.')[0].split('_')[-1]
            if validChkStr == self.infoDict['expCnt']:
                resFile = os.path.join(fPath, resF)
                break
        print(resFile)

        df = pd.read_csv(resFile)
        inCorrAnsIdx = df.index[df['res'] == 0].tolist() # 틀린문제 index 추출
        corrAnsIdx = df.index[df['res'] == 1].tolist() # 맞춘문제 index 추출

        df_inCorr = df.copy().iloc[inCorrAnsIdx, :] # 틀린문제 DataFrame 생성
        df_corr = df.copy().iloc[corrAnsIdx, :] # 맞춘문제 DataFrame 생성

        # 다음 행에 존재하는 conf val을 한 행으로 합치기
        for inCorrIdx, corrIdx in zip_longest(inCorrAnsIdx, corrAnsIdx):
            if inCorrIdx is not None:
                df_inCorr.at[inCorrIdx, 'confidence'] = df.at[inCorrIdx + 1, 'confidence']
            if corrIdx is not None:
                df_corr.at[corrIdx, 'confidence'] = df.at[corrIdx + 1, 'confidence']

        print(df_inCorr.head(), '\n', df_corr.head())


        inCorrCnt, corrCnt = df_inCorr.shape[0], df_corr.shape[0]
        print('틀린문제: ', inCorrCnt,
              '\n정답률: ', corrCnt/5)
