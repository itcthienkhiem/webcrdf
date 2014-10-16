"""
Django settings for webcrdf project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import glob
import cv2
import numpy as np
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import appcbir.alg as algCBIR
import appsegmxr.alg as algSegmXR


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '11111111111111111111111111111111111111111111111111'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appcbir',
    'appxray',
    'appsegmxr',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
##    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'webcrdf.urls'

WSGI_APPLICATION = 'webcrdf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/data/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'data'),
##    os.path.join(BASE_DIR, 'datadb.cbir'),
##    os.path.join(BASE_DIR, 'datadb.xray'),
)


#### Loading CBIR CT-data
STATIC_DB_DIR="datadb.cbir/dbdir_ct_10k"
STATIC_ROOT_DATADB=os.path.join(BASE_DIR, 'data/datadb.cbir/dbdir_ct_10k')
##STATIC_ROOT_USER  =os.path.join(BASE_DIR, 'data/users')
STATIC_ROOT_IMG   =os.path.join(BASE_DIR, 'data/images')
STATIC_ROOT_USERDATA_CBIR  =os.path.join(BASE_DIR, 'data/users_cbir')
if not os.path.isdir(STATIC_ROOT_USERDATA_CBIR):
    os.mkdir(STATIC_ROOT_USERDATA_CBIR)

CBIR=algCBIR.SCBIR(STATIC_ROOT_DATADB)
CBIR.load()
##CBIR.printInfo()

#### Loading X-Ray data
STATIC_ROOT_XRAY_USERDATA  =os.path.join(BASE_DIR, 'data/users_xray')
STATIC_ROOT_XRAY_DBDATA    =os.path.join(BASE_DIR, 'data/datadb.xray')
if not os.path.isdir(STATIC_ROOT_XRAY_USERDATA):
    os.mkdir(STATIC_ROOT_XRAY_USERDATA)
IMAGEDB=[]
IMAGEDB_DATA=[]
IMAGEDB_DPTS=[]
for ii in glob.glob('%s/data/datadb.xray/*.png' % BASE_DIR):
    img=cv2.imread(ii, 0) ##cv2.CV_LOAD_IMAGE_GRAYSCALE)
    fpts="%s_pts.csv" % ii
    if img!=None:
        tmp={'w': img.shape[1], 'h': img.shape[0], 'url': '/data/datadb.xray/%s' % os.path.basename(ii), 'idx': os.path.basename(ii)}
        # IMAGEDB.append((img, tmp))
        IMAGEDB.append(tmp)
        IMAGEDB_DATA.append(img)
        IMAGEDB_DPTS.append(np.genfromtxt(fpts, delimiter=','))

#### Loading data X-Ray segmentation
STATIC_ROOT_SEGMXR_USERDATA=os.path.join(BASE_DIR, 'data/users_segmxr')
STATIC_ROOT_SEGMXR_DBDATA  =os.path.join(BASE_DIR, 'data/datadb.segmxr')
if not os.path.isdir(STATIC_ROOT_SEGMXR_USERDATA):
    os.mkdir(STATIC_ROOT_SEGMXR_USERDATA)
taskManagerSegmXR = algSegmXR.TaskManagerSegmXR(nproc=2)
taskManagerSegmXR.loadData(STATIC_ROOT_SEGMXR_DBDATA)

regXray = algSegmXR.RegisterXray()
regXray.loadDB(STATIC_ROOT_SEGMXR_DBDATA)
regXray.numNGBH=1