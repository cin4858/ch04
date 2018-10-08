

# 3. 실전 프로그램 개발 - Blog 앱

- bookmark = 책갈피 = 바로가기  
- bog = web log = 웹에서 작성하는 일지 = 웹 게시판
- 블로그 웹 애플리케이션(앱)
  - 웹 프로그래밍 학습자를 위한 필수 예제
  - 글(포스트) 등록/수정/삭제/열람
  - 태그 달기, 댓글 달기, 검색, 콘텐츠 생성/편집
  - 3장에서는 포스트 등록/열람 기능만 우선 개발

- 장고 MTV 패턴
  - model     (DB)
  - template  (화면, HTML/CSS)
  - view      (논리 제어 프로그램)

***
# 3.1 애플리케이션 설계

## 3.1.1 화면 UI 설계 (교과서 64쪽)
- post_all.html     (모든 포스트를 리스트 형태로 출력)
  ![post_all.html 화면](post_all.png)
- post_detail.html  (특정 포스트를 내용 보기 형태로 출력)
  ![post_detail.html 화면](post_detail.png)
- post_archive.html  (포스트 모음 형태로 출력)
  ![post_archive.html 화면](post_archive.png)

## 3.1.2 테이블 설계
- models.py에 코딩
- 블로그 앱에 필요한 Post 모델 클래스 설계

  | 필드 이름 | 유형 |제약 | 설명 |
  |:---       |:----|:--- |:--- |
  |id         | Integer       |PK, Auto Increment |기본키 |
  |title      | CharField(50) |                   | 포스트 제목 |
  |slug       | SlugField(50) |Unique             | 포스트 제목 별칭 |
  |description| CharField(150)|Blank              | 포스트 내용 한 줄 설명 |
  |content    | TextFeild     |                   | 포스트 내용 |
  |create_date| DateTimeField |auto_now_add       | 포스트 최초 등록 일시 |
  |modify_date| DateTimeField |auto_now           | 포스트 최후 수정 일시 |

## 3.1.3 로직 설계
  - URL 설계로 대치

## 3.1.4 URL 설계

|<center>URL 패턴</center>| <center>View</center> | <center>Template</center>
|:--------                |:--------              |--------:                  
| /blog/                  | PostLV(ListView)        |*post_all.html^1^*        
| /blog/post              | PostLV(ListView)        |*post_all.html^1^*        
| /blog/post/django-example^2^/| PostDV(DetailView) |*post_detail.html*      
| /blog/archive/          | PostAV(ArchiveIndexView)|*post_archive.html*    
| /blog/2012/             | PostYAV(YearArchiveView)|*post_archive_year.html*    
| /blog/2012/nov/        | PostMAV(MonthArchiveView)|*post_archive_month.html*    
| /blog/2012/nov/10/^3^   | PostDAV(DayArchiveView) |*post_archive_day.html*    
| /blog/today/          | PostTAV(TodayArchiveView) |*post_archive_day.html*    
| /admin/                 | (장고 제공 기능)        |        
| /bookmark/              | (ch02 제공 기능)        |        
| /bookmark/3/            | (ch02 제공 기능)        |        
| /bookmark/t_CBV/^4^      | (ch02 제공 기능)        |        
| /bookmark/t_FBV/^5^      | (ch02 제공 기능)        |        

^1^ 템플릿 이름을 post_list.html이 아닌 post_all.html로 지정하였음
^2^ "django-example"과 같은 단어를 slug라고 하는데, 기본키 대용으로 자주 사용함
^3^ "2012년 11월 10일"이라는 의미
^4^ "/bookmark_t_CBV/" 형태를 "/bookmark/t_CBV/" 형태로 수정
^5^ "/bookmark_t_FBV/" 형태를 "/bookmark/t_FBV/" 형태로 수정

## 3.1.5 작업/코딩 순서

|  <center>순서</center> |  <center>명령/파일</center>  |  <center>작업 내용</center> |
|--------            |:--------                |:--------                |
|**뼈대 만들기**      | startproject            |(ch02에서 이미 작업, 생략)|
| <center>"</center> | settings.py             |<center>"</center>|
| <center>"</center> | migrate                 |<center>"</center>|
| <center>"</center> | createsuperuser         |<center>"</center>|
| <center>"</center> | startapp                |*블로그 앱 생성*        |
| <center>"</center> | settings.py             |*블로그 앱 등록*        |
|**모델 코딩**      | models.py                |*모델(테이블) 정의*        |
|<center>"</center>| admin.py                 |*관리자 사이트에 모델 등록*        |
|<center>"</center>| makemigrations           |*DB에 모델 반영 준비*        |
|<center>"</center>| migrate                  |*DB에 모델 반영 실행*        |
|**URLconf 코딩**  | urls.py                 |*URL 패턴 정의*        |
|**뷰 코딩**       | views.py                 |*뷰 로직 작성*        |
|**템플릿 코딩**   | templates 폴더                |*템플릿 파일 작성*        |
|**기타 코딩**    | -                |*-*        |


***
# 3.2 개발 코딩
## 3.2.1 뼈대 만들기
- 블로그 앱 생서 (startapp 작업)
  - manage.py 파일이 존재하는 작업 폴더에서 startapp 작업을 수행하면,
    해당 폴더에 blog 앱 폴더가 생성됨
    ```bash
    (myvenv) C:\work>python manage.py startapp bookmark
    ```
  - blog\apps.py 및 bookmark\apps.py 파일은 앱 설정 파일,
    mysite\settings.py 파일은 프로젝트 설정 파일
- 블로그 앱 등록 (mysite\settings.py)
  ```python {.line-numbers}
  # 이전 생략
  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookmark.apps.BookmarkConfig',     # (ch02) bookmark 앱을 추가 등록
    'blog.apps.BlogConfig',             # (ch03) blog 앱을 추가 등록
  ]
  # 이후 생략
  ```
## 3.2.2 모델 코딩
- 모델 정의 blog\models.py
  ```Python {.line-numbers}
  # 문자열 처리 방식이 상이한 파이썬 버전 2 및 3의 호환성을 위한 임포트
  from __future__ import unicode_literals
  from django.utils.encoding import python_2_unicode_compatible

  from django.db import models
  # url 패턴을 만들어주는 장고 내장 함수 reverse()를 위한 임포트
  from django.core.urlresolvers import reverse

  # Create your models here.

  @python_2_unicode_compatible
  class Post(models.Model):
      # 아래에서 관리자 화면의 레이블과 도움말은 모두 한글로 수정하였음(교과서에서는 대문자 영문이었음)
      # 한 줄로 입력되는 CharField
      title = models.CharField('제목', max_length=50)
      slug = models.SlugField('슬러그',  # 기본 길이 50, 인덱스가 기본 생성됨,
                                         # 제목에서 주요 단어를 하으픈으로 연결하여 생성
                              unique=True,  # unique 설정, 기본키 대용으로 사용 가능
                              allow_unicode=True,  # 한글 입력 가능하도록
                              help_text='제목에 대한 한 단어의 별명.')
      description = models.CharField('설명',
                                     max_length=100,
                                     blank=True,  # 블랭크 허용
                                     help_text='간략한 설명 문구.')
      content = models.TextField('내용')  # TextField이므로 여러 줄 입력 가능함
      create_date = models.DateTimeField('최초 생성 일시',
                                         auto_now_add=True)  # 최초 생성 일시를 자동 저장하도록
      modify_date = models.DateTimeField('최종 수정 일시',
                                         auto_now=True)  # 최종 수정 일시를 자동 저장하도록

      class Meta:  # 필드 속성 외에 필요한 파라미터를 Meta 내부 클래스로 정의
          verbose_name = '기사'              # 'post'
          verbose_name_plural = '기사 모음'  # 'posts'
          db_table  = 'my_posts'           # DB에 저장할 테이블 이름을 my_posts'라고 지정
                                           # 기본값(앱이름_모델클래스이름)은 'blog_post'
          ordering  = ('-modify_date',)  # 최종 수정 일시의 내림차순 정렬

      def __str__(self):
          return self.title  # 객체를 출력할 때 제목만 출력

      def get_absolute_url(self): # 이 메소드가 정의된 객체를 지칭하는 URL을 반환
          # 아래에서 'blog:post_detail'는 blog 앱 이름공간의 post_detail이란 의미
          # # Example: /post/django-example/
          # url(r'^post/(?P<slug>[-\w]+)/$', PostDV.as_view(), name='post_detail'),          
          return reverse('blog:post_detail', args=(self.slug,))

      def get_previous_post(self):  # 3.2.5 항에서 템플릿 작성할 때 사용
          return self.get_previous_by_modify_date()

      def get_next_post(self):  # 3.2.5 항에서 템플릿 작성할 때 사용
          return self.get_next_by_modify_date()
  ```

- 관리자 사이트에 테이블 등록 blog\admin.py
  ```python {.line-numbers}
  from django.contrib import admin
  from blog.models import Post

  # Register your models here.

  # blog.models.Post 클래스를 관리자 사이트에서 보여주는 방식 정의
  class PostAdmin(admin.ModelAdmin):
      list_display  = ('title', 'modify_date') # 관리자 화면에 보여줄 필드 지정
      list_filter   = ('modify_date',)  # 필터 사이드바를 출력
      search_fields = ('title', 'content')  # 검색 박스 표시하되, 입력된 값을 여기서 검색하라고 지정
      prepopulated_fields = {'slug': ('title',)}  # 슬러그 필드가 제목 필드의 값으로 자동 작성되도록 지정

  admin.site.register(Post, PostAdmin)  # Post 및 PostAdmin 클래스를 관지자 사이트에 등록
  ```
- DB 현행화
  ```bash
  (myvenv) C:\work>python manage.py makemigrations    # DB 갱신 준비
  (myvenv) C:\work>python manage.py migrate           # DB 갱신 실행
  ```
- 웹 서버 기동
  ```shell
  (myvenv) C:\work>python manage.py runserver
  ```
- [수퍼유저 암호 변경](http://iyc1030.tistory.com/entry/PythonDjango-Admin-SuperUser-%EC%9D%BC%EB%B0%98-User-%ED%8C%A8%EC%8A%A4%EC%9B%8C%EB%93%9C-%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8-%EB%B3%80%EA%B2%BD)
- 관리자 사이트 확인
  - 웹 브라우저에서 http://localhost:8000/admin 또는 http://127.0.0.1:8000/admin 접속
  ![어드민 사이트 화면](adminSite.png)
  ![블로그 어드민 화면](admin1stPost.png)
  ![사이드 필터 화면](adminSideFilter.png)
***

## 3.2.3 URLconf 코딩
- URLconf 작성 방법
  - mysite\urls.py 단일 파일로 작성하는 방법(간단한 예제의 경우)
  - ROOT_URLCONF(mysite\urls.py) 및 APP_URLCONF(앱\urls.py)로 구분하여 작성하는 방법
- mysite\urls.py
  ```Python {.line-numbers}
  # 장고 내장 함수 include() 및 url() 임포트
  from django.conf.urls import include, url
  from django.contrib import admin

  # 이 부분은 bookmark.urls 부분으로 옮겼음
  # from bookmark.views import BookmarkLV, BookmarkDV

  urlpatterns = [
      # admin.site.urls를 include(admin.site.urls)로 변경했으나 사실 동일한 효과를 발휘
      # 다른 앱에서 정의된 url 설정을 재활용할 때 include() 함수를 써야 하지만,
      # 예외적으로 admin.site.urls에 대해서는 include() 함수를 생략해도 무방함
      url(r'^admin/', include(admin.site.urls)),

      # 아래 두 url 패턴에서 뒷 부분에 패턴의 끝을 표시하는 '$' 문자가 없음!!!

      url(r'^bookmark/', include('bookmark.urls', namespace='bookmark')),
      # bookmark.urls를 적용하고, 이름공간을 'bookmark'로 지정
      url(r'^blog/', include('blog.urls', namespace='blog')),
      # blog.urls를 적용하고, 이름공간을 'blog'로 지정
  ]
  ```
- bookmark\urls.py
  ```Python {.line-numbers}
  from django.conf.urls import url
  # from bookmark.views import BookmarkLV, BookmarkDV # 교과서 ch02 52쪽의 원래 코드를 아래와 같이 수정함
  from . import views  # 이렇게 수정하면 아래 코드에서와 같이 views.~ 형식으로 변경해야 함
  urlpatterns = [
      # ch02에서 코딩했던 부분을 아래와 같이 수정하였으므로 주석 처리함
      # # 북마크 앱을 위한 클래스 기반 뷰
      # # /bookmark/ 요청을 처리할 뷰 클래스를 BookmarkLV로 지정하고, URL 패턴 이름 지정
      # url(r'^bookmark/$', views.BookmarkLV.as_view(), name='index'),
      # # /bookmark/숫자/ 요청을 처리할 뷰 클래스를 BookmarkDV로 지정하고, URL 패턴 이름 지정
      # url(r'^bookmark/(?P<pk>\d+)/$', views.BookmarkDV.as_view(), name='detail'),
      # # tabular list
      # url(r'^bookmark_t_FBV/$', views.tabularBookmark, name='index_t_FBV'),
      # url(r'^bookmark_t_CBV/$', views.BookmarkLV.as_view(), name='index_t_CBV'),

      # 북마크 앱을 위한 클래스 기반 뷰
      # /bookmark/ 요청을 처리할 뷰 클래스를 BookmarkLV로 지정하고, URL 패턴 이름 지정
      # url(r'^bookmark/$', views.BookmarkLV.as_view(), name='index'),
      # ch02 코드는 위와 같았으나, 아래처럼 수정함
      # 왜냐하면, mysite.urls에서 '^bookmark/' 부분과 일치하는 request.path 부분이 처리되고,
      # 처리된 부분이 제거된 나머지 request.path 부분만 bookmark.urls로 전달되므로!!!
      url(r'^$', views.BookmarkLV.as_view(), name='index'),
      # /bookmark/숫자/ 요청을 처리할 뷰 클래스를 BookmarkDV로 지정하고, URL 패턴 이름 지정
      # url(r'^bookmark/(?P<pk>\d+)/$', views.BookmarkDV.as_view(), name='detail'),
      url(r'^(?P<pk>\d+)/$', views.BookmarkDV.as_view(), name='detail'),
      # tabular list
      # url(r'^bookmark_t_FBV/$', views.tabularBookmark, name='index_t_FBV'),
      # url 패턴 매칭을 '/' 단위로 처리하기 위하여 아래와 같이 수정
      # 이에 따라서 템플릿에서도 수정이 필요함
      url(r'^t_FBV/$', views.tabularBookmark, name='index_t_FBV'),
      # url(r'^bookmark_t_CBV/$', views.BookmarkLV.as_view(), name='index_t_CBV'),
      # url 패턴 매칭을 '/' 단위로 처리하기 위하여 아래와 같이 수정
      # 이에 따라서 템플릿에서도 수정이 필요함
      url(r'^t_CBV/$', views.BookmarkLV.as_view(), name='index_t_CBV'),
  ]  
  # 주의할 점
  # bookmark.urls 내부에서 지정한 url 패턴의 이름 'index', 'detail', ... 등을
  # 템플릿에서 사용할 때, 이름공간 bookmark를 포함하도록
  # 'bookmark:index','bookmark:detail', ... 등으로 변경해주어야 함!!!
  ```
- blog\urls.py
  ```Python {.line-numbers}
  from django.conf.urls import url
  from blog.views import * # 이렇게 수정하면 아래와 같이 views.~ 형식에서 views. 부분을 빼야 함
                           # bookmark.urls에서는 from . import views로 했으므로 views.~ 형식으로 사용해야 함
                           # * 표시는 모든 멤버를 일괄 지정함      
  urlpatterns = [

      # Example: /
      url(r'^$',      PostLV.as_view(), name='index'),  
      # Example: /post/ (same as /)
      url(r'^post/$', PostLV.as_view(), name='post_list'),

      # Example: /post/django-example/
      url(r'^post/(?P<slug>[-\w]+)/$', PostDV.as_view(), name='post_detail'),

      # Example: /archive/
      url(r'^archive/$', PostAV.as_view(), name='post_archive'),

      # Example: /2012/
      url(r'^(?P<year>\d{4})/$', PostYAV.as_view(), name='post_year_archive'),

      # Example: /2012/nov/
      url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', PostMAV.as_view(), name='post_month_archive'),

      # Example: /2012/nov/10/
      url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$', PostDAV.as_view(), name='post_day_archive'),

      # Example: /today/
      url(r'^today/$', PostTAV.as_view(), name='post_today_archive'),
  ]
  # 위에서 지정한 name 항목을 템플릿에서 사용할 때에는 이름공간을 포함하여,
  # blog:index, blog:post_list, blog:post_detail, blog:post_archive, ... 로 명시해야 함
  ```
***
## 3.2.4 뷰 코딩
- 클래스형 제네릭 뷰: ListView, DetailView
- 날짜 제네릭 뷰: ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, TodayArchiveView
- blog\views.py
  ```python {.line-numbers}
  # 뷰 작성에 필요한 클래스형 제넥릭 뷰 임포트
  from django.views.generic import ListView, DetailView
  # 뷰 작성에 필요한 날짜 제네릭 뷰 임포트
  from django.views.generic.dates import ArchiveIndexView, \
      YearArchiveView, MonthArchiveView, DayArchiveView, TodayArchiveView
  # blog.models.Post 클래스 임포트
  from blog.models import Post

  # ListView를 상속받아서 PostLV 작성
  class PostLV(ListView) :
      model = Post
      # 기본값 'blog/post_list.html' 대신 지정 (3.1.4 URL 설계 항 참고)
      template_name = 'blog/post_all.html'
      # 컨텍스트 객체 이름을 기본값(object_list)와 다르게 지정했지만,
      # 기본값(object_list)도 여전히 사용 가능함
      context_object_name = 'posts'
      paginate_by = 2  # 페이지 당 2 개 객체를 처리하도록 지정

  # DetailView를 상속받아서 PostDV 작성
  # 기본키 대신 slug를 전달 받고, 나머지 속성은 기본값 사용
  # slug는 URLconf가 전달해줌(3.1.4 URL 설계 항 참고)
  class PostDV(DetailView) :
      model = Post

  # 모든 아카이브 클래스에서 기준 날짜(date_filed) 속성을 modify_date로 지정

  # ArchiveIndexView를 상속받아서 PostAV 작성
  class PostAV(ArchiveIndexView) :
      model = Post
      date_field = 'modify_date'

  # YearArchiveView를 상속받아서 PostYAV 작성
  class PostYAV(YearArchiveView) :
      model = Post
      date_field = 'modify_date'
      make_object_list = True    # 기본값은 False이지만,
      # object_list 컨텍스트 변수를 생성해서 템플릿에 전달하도록 지시
      # URLconf에서 추출한 연도 값을 전달받아서 object_list를 구성하고
      # 이를 템플릿에 전달함

  # MonthArchiveView를 상속받아서 PostMAV 작성
  class PostMAV(MonthArchiveView) :
      model = Post
      date_field = 'modify_date'
      # URLconf에서 추출한 연도 및 월 값을 전달받아서 object_list를 구성하고
      # 이를 템플릿에 전달함

  # DayArchiveView를 상속받아서 PostDAV 작성
  class PostDAV(DayArchiveView) :
      model = Post
      date_field = 'modify_date'
      # URLconf에서 추출한 연도, 월, 일 값을 전달받아서 object_list를 구성하고
      # 이를 템플릿에 전달함

  # TodayArchiveView를 상속받아서 PostTAV 작성
  class PostTAV(TodayArchiveView) :
      model = Post
      date_field = 'modify_date'
      # URLconf에서 지정한 당일(today)에 해당하는 object_list를 구성하고
      # 이를 템플릿에 전달함  
  ```
***

## 3.2.5 템플릿 코딩

### 3.2.5.1 post_all.html

![post_all.html 화면](post_all.png)
- blog\templates\blog\post_all.html
```html {.line-numbers}
<!--특별한 HTML 태그 지정이 없으면 장고가 <body> </body> 영역으로 간주함-->
<h1>Blog List</h1>

<!--blog.views.PostLV.context_object_name='posts'라고
기본값 object_list 대신 정의했지만, object_list 역시 사용 가능함-->
{% for post in posts %}
    <h2>
        <!--href='blog/post/django-example/'과 같은 슬러그 형태로 링크 처리하되,
        {{ blog.models.Post.get_absolute_url() 함수 }} 또는  
        {% url url_name pk %}}로 링크 처리-->
        <a href='{{ post.get_absolute_url }}'>
        <!--위 a 요소와 아래 a 요소는 동일한 코드이지만,
        위는 url 패턴을 간접 태그 인자로 사용하지만,
        아래는 url 패턴을 직접 태그 인자로 사용함 -->
        <!--<a href="{% url 'blog:post_detail' post.slug %}}">-->            
            {{ post.title }}
        </a>
    </h2>
    <!--post.modify_date를 date:"N d, Y" 형식으로 출력 (예: July 05, 2015) cf. http://oddly.tistory.com/64-->
    {{ post.modify_date|date:"N d, Y" }}
    <p>{{ post.description }}</p>
{% endfor %}

<br/>

<!--이전/현재/다음 페이지 이동 -->
<div> <!--div 요소는 블록 요소-->
    <span>  <!--span 요소는 인라인 요소-->
        <!--page_obj는 장고 Page 객체가 들어있는 컨텍스트 변수이며
        has_previous, has_next, previous_page_number, next_page_number,
        number, pagenator.num_pages 속성을 가짐-->
        {% if page_obj.has_previous %}
            <!--링크 형식 href="?page={{ page_obj.previous_page_number }}"에 주목-->
            <a href="?page={{ page_obj.previous_page_number }}">이전 페이지</a>
        {% endif %}

        페이지 {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}

        {% if page_obj.has_next %}
            <!--링크 형식 href="?page={{ page_obj.previous_page_number }}"에 주목-->
            <a href="?page={{ page_obj.next_page_number }}">다음 페이지</a>
        {% endif %}
    </span>
</div>
```

### 3.2.5.2 post_detail.html
  ![post_detail.html 화면](post_detail.png)
- blog\templates\blog\post_detail.html
```html {.line-numbers}
<!--특별한 HTML 태그 지정이 없으면 장고가 <body> </body> 영역으로 간주함-->
<!--아래에서 object 객체는 PostDV 클래스 형 뷰에서
컨텍스트 변수로 넘겨주는 Post 클래스의 특정 객체-->

<!--object.title을 H2 요소로 출력 -->
<h2>{{ object.title }}</h2>

<p class="other_posts">
    <!--object.get_previous_by_modify_date 함수는 modify_date 기준으로 이전 객체를 반환-->
    {% if object.get_previous_by_modify_date %}
        <!--blog.Post.get_previous_post 함수는 이전 객체를 반환 -->
        <!--get_absolute_url 함수는 /blog/post/slug단어 형태의 URL 패턴을 반환-->
        <!--'&laquo;'는 HTML 특수 문자 '<<'를 의미함-->
        <a href="{{ object.get_previous_post.get_absolute_url }}" title="View previous post">
            &laquo;--{{ object.get_previous_post }}
        </a>
    {% endif %}

    {% if object.get_next_by_modify_date %}
        |
        <!--blog.Post.get_next_post 함수는 다음 객체를 반환 -->
        <!--get_absolute_url 함수는 /blog/post/slug단어 형태의 URL 패턴을 반환-->
        <!--'&raquo;'는 HTML 특수 문자 '>>'를 의미함-->
        <a href="{{ object.get_next_post.get_absolute_url }}" title="View next post">
            {{ object.get_next_post }}--&raquo;
        </a>
    {% endif %}
</p>
<!--object.modify_date를 파이프(|)를 통하여 date:"j F Y" 형식으로 출력-->
<p class="date">{{ object.modify_date|date:"j F Y" }}</p>
<br/>

<div class="body">
    <!--object.content를 파이프(|)를 통하여 linebreaks 탬플릿 필터로 처리하여
     개행문자'\n'를 인식하도록 조치함-->
    {{ object.content|linebreaks }}
</div>
```

### 3.2.5.3 post_archive.html

![post_archive.html 화면](post_archive.png)
- blog\templates\blog\post_archive.html
```html {.line-numbers}
<!--{% now %} 템플릿 태그는 현재 일시를 "N d, Y" 형식(July 18, 2015)으로 출력  -->
<h1>{% now "N d, Y" %}까지의 게시글 모음</h1>
<ul>
    <!--date_list 컨텍스트 변수는 DateQuerySet 객체 리스트를 담고 있으며, 여기에는-->
    <!--QuerySet에서 날짜 정보만을 추출해서 datetime.date 유형의 객체로 저장함 -->    
    {% for date in date_list %}
        <!--연도 리스트를 inline 방식으로 출력-->
        <li style="display: inline;">
            <a href="{% url 'blog:post_year_archive' date|date:'Y' %}">
                {{ date|date:"Y" }} 년
            </a>
        </li>
    {% endfor %}
</ul>
<br/>
<div>
    <ul>
        <!--기본 컨텍스트 변수로 object_list 및 lates 모두 가능함-->
        {% for post in object_list %}
            <li>
                순서 없는 리스트로 게시글 수정일과 제목을 공백 3개로 구분하여 출력
                {{ post.modify_date|date:"Y-m-d" }}&nbsp;&nbsp;&nbsp;
                <a href="{{ post.get_absolute_url }}">
                    <strong>{{ post.title }}</strong>
                </a>
            </li>
        {% endfor %}
    </ul>
</div>
```

### 3.2.5.4 post_archive_year.html
![post_archive_year.html 화면](post_archive_year.png)
- blog\templates\blog\post_archive_year.html
```html {.line-numbers}
<h1>{{ year|date:"Y" }}년 게시글 모음</h1>

<ul>
    <!--date_list 컨텍스트 변수는 DateQuerySet 객체 리스트를 담고 있으며, -->
    <!--여기에는 QuerySet에서 날짜 정보만을 추출해서 datetime.date 유형의 객체로 저장함 -->
    {% for date in date_list %}
    <li style="display: inline">
        <!--'blog:post_month_archive' url에 링크 연결하되, 2015(년) 및 7(월) 형식으로 매개변수를 전달-->
        <a href="{% url 'blog:post_month_archive' year|date:'Y' date|date:'b' %}">
            <!--월 제목을 "F" 형태(예: July)로 출력 -->
            {{ date|date:"F" }}
        </a>
    </li>
    {% endfor %}
</ul>
<br/>

게시글 리스트 출력 부분은 post_archive.html과 동일한 방식
<div>
    <ul>
        <!--기본 컨텍스트 변수로 object_list 및 lates 모두 가능함-->
        <!--latest는 ArchiveIndexView에서만 정의된 변수이므로 여기서는 사용 불가-->
        {% for post in object_list %}
        <li>
            {{ post.modify_date|date:"Y-m-d" }}&nbsp;&nbsp;&nbsp
            <a href="{{ post.get_absolute_url }}">
                <strong>{{ post.title }}</strong>
            </a>
        </li>
        {% endfor %}
    </ul>
</div>
```

### 3.2.5.5 post_archive_month.html
![post_archive_month.html 화면](post_archive_month.png)
- blog\templates\blog\post_archive_month.html
```html {.line-numbers}
<h1>{{ month|date:"Y년 m월" }} 게시글 모음</h1>

<div>
    <ul>
        {% for post in object_list %}
        <li>
            {{ post.modify_date|date:"Y-m-d" }}&nbsp;&nbsp;&nbsp;
            <a href="{{ post.get_absolute_url }}">
                <strong>{{ post.title }}</strong>
            </a>
        </li>
        {% endfor %}
    </ul>
</div>
```

### 3.2.5.6 post_archive_day.html
![post_archive_day.html 화면](post_archive_day.png)
- blog\templates\blog\post_archive_day.html
```html {.line-numbers}
<h1>{{ day|date:"Y년 b월 d일"}} 게시글 모음</h1>

<div>
    <ul>
        {% for post in object_list %}
        <li>
            {{ post.modify_date|date:"Y-m-d" }}&nbsp;&nbsp;&nbsp;
            <a href="{{ post.get_absolute_url }}">
                <strong>{{ post.title }}</strong>
            </a>
        </li>
        {% endfor %}
    </ul>
</div>
```
- post_archive_day.html과 post_archive_year.html은 페이지 제목만 다르고 나머지는 동일함
- TodayArchiveView 및 DayArchiveView 제네릭 뷰는 기본 템플릿 파일 이름이 동일하므로
  TodayArchiveView에 대한 템플릿 파일은 작성이 필요하지 않음
***

# 4. Git 및 PythonAnywhere 작업
## 4.1 Git 작업
- ch02에서 수행한 아래 작업은 최초 한번만 수행하면 되므로 생략
  - Git 설치
  - Git 저장소 초기화
  - work\.gitignore 파일 작성
  - Git 저장소 상태 확인 및 등록
  - https://github.com 새 리포지토리 생성 및 최초 배포
  - Git add 및 push

## 4.2 pythonanywhere 작업
- ch02에서 수행한 아래 작업은 최초 한번만 수행하면 되므로 생략
  - http://www.pythonanywhere.com 회원 가입  
  - bash console에서 git clone 작업
  - 웹 앱으로 블로그 배포
  - 가상환경 설정
  - WSGI 파일 설정
  - Web 탭에서 큰 녹색 다시 불러오기(Reload) 버튼 클릭 후, 페이지 최상단 링크로 브라우징

## 4.3 ch03 이후 로컬 작업 (push)   
  ```shell
  (myvenv) C:\work>git status
  (myvenv) C:\work>git add --all .
  (myvenv) C:\work>git status
  (myvenv) C:\work>git commit -m "Changed ..."
  (myvenv) C:\work>git push
  ```

## 4.4 ch03 이후 서버 작업 (pull)
  ```shell
  $ cd my-first-blog
  $ git pull
  ```
  - Web tab에서 Reload
  - http://logistex2018.pythonanywhere.com/bookmark/
  - http://logistex2018.pythonanywhere.com/blog/
  ***
