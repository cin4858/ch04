# from django.shortcuts import render

from django.views.generic import ListView, DetailView
# 모델 클래스 임포트
from bookmark.models import Bookmark

# 북마크 테이블의 전체 레코드 리스트 출력을 위한 뷰
class BookmarkLV(ListView):
    model = Bookmark
    # 1) 디폴트 컨텍스트 변수 object_list를 적용
    #  2) 디폴트 템플릿 파일명 소문자모델명_list.html = bookmark_list.html

# 북마크 테이블의 특정 레코드 상세 출력을 위한 뷰
class BookmarkDV(DetailView):
    model = Bookmark
    # 1) 디폴트 컨텍스트 변수 object를 적용
    #  2) 디폴트 템플릿 파일명 소문자모델명_detail.html = bookmark_detail.html     #    기본 키로 조회하는 경우, 모델 클래스 명만 지정하면,
    #r'^bookmark/(?P<pk>)\d+)/$' # 에 따라서 기본 키 값이 자동으로 인수 전달됨
class tabularBookmark(ListView):
    model = Bookmark
