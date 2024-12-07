import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from pool.BluesMaterialIO import BluesMaterialIO

class MaterialParaImage(CrawlerHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__download(request)

  def __download(self,request):
    material = request.get('material')
    paras = material.get('material_body')
    material_thumbnail = material.get('material_thumbnail')
    image_count = 0
    for para in paras:
      # download and deal image
      if para['type'] == 'image':
        image_count += 1
        para['value'] = BluesMaterialIO.get_download_image(material,para['value'])
    
    # make sure have at least one image
    if not image_count:
      paras.append({'type':'image','value':material_thumbnail})

