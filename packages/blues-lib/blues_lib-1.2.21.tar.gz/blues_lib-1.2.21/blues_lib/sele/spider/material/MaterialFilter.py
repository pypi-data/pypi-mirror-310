import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from pool.BluesMaterialIO import BluesMaterialIO  

class MaterialFilter(CrawlerHandler):
  '''
  Remove the unavailable breifs
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__filter(request)

  def __filter(self,request):
    material = request.get('material')
    if not BluesMaterialIO.is_legal_material(material):
      request['material'] = None


