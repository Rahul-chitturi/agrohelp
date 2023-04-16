from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('admin/login',views.adminLogin,name='adminLogin'),
    path('admin/logout',views.adminLogout,name='adminLogout'),
    path('admin/adminMenu',views.adminMenu,name='adminMenu'),
    path('admin/usersList',views.usersList,name='usersList'),
    path('admin/blockUser',views.blockUser,name='blockUser'),
    path('admin/adminRegister',views.adminRegister,name='adminRegister'),
    path('admin/deleteAdmin',views.deleteAdmin,name='deleteAdmin'),
    path('admin/adminList',views.adminList,name='adminList'),
    path('admin/ordersList',views.ordersList,name='ordersList'),
    path('admin/applicationsList',views.applicationsList,name='applicationsList'),
    path('admin/productsList',views.productsList,name='productsList'),
    path('admin/addProduct', views.addProduct, name='addProduct'),
    path('admin/editProduct',views.editProduct,name='editProduct'),
    path('admin/editProductDetails',views.editProductDetails,name='editProductDetails'),
    path('admin/deleteProduct',views.deleteProduct,name="deleteProduct"),
    path('admin/schemesList',views.schemesList,name='schemesList'),
    path('admin/addScheme',views.addScheme,name='addScheme'),
    path('admin/editScheme',views.editScheme,name='editScheme'),
    path('admin/editSchemeDetails',views.editSchemeDetails,name='editSchemeDetails'),
    path('admin/deleteScheme',views.deleteScheme,name='deleteScheme'),
    path('admin/agroBasicList',views.agroBasicList,name='agroBasicList'),
    path('admin/feedbacksList',views.feedbacksList,name='feedbacksList'),
    path('admin/addBasic',views.addBasic,name='addBasic'),
    path('admin/viewDocument',views.viewDocument,name='viewDocument'),
    path('admin/deleteAgroBasic',views.deleteAgroBasic,name='deleteAgroBasic'),
    path('admin/orderDetails',views.orderDetails,name='orderDetails'),
    path('admin/deleteOrder',views.deleteOrder,name='deleteOrder'),
    path('admin/editOrder',views.editOrder,name='editOrder'),
    path('admin/editOrderDetails',views.editOrderDetails,name='editOrderDetails'),
    path('admin/subscribersList',views.subscribersList,name='subscribersList'),
    path('admin/deleteSubscription',views.deleteSubscription,name='deleteSubscription'),
    path('admin/deleteGrassCutter',views.deleteGrassCutter,name='deleteGrassCutter'),
    path('admin/grassCuttersList',views.adminGrassCuttersList,name='adminGrassCuttersList'),


    path('',views.home,name='home'),
    path('team',views.team,name='team'),
    path('contactUs',views.contactUs,name='contactUs'),
    path('subscribe',views.subscribe,name='subscribe'),
    path('services',views.services,name='services'),
    path('equipments',views.equipments,name='equipments'),
    path('fertilizers',views.fertilizers,name='fertilizers'),
    path('schemes',views.schemes,name="schemes"),

    path('user/login',views.userLogin,name='userLogin'),
    path('user/logout',views.userLogout,name='userLogout'),
    path('user/register',views.userRegister,name='userRegister'),
    path('user/completeSetup',views.completeSetup,name='completeSetup'),
    path('user/profile',views.userProfile,name='userProfile'),
    path('user/feedback',views.feedbackForm,name='feedbackForm'),
    path('user/cart',views.myCart,name="myCart"),
    path('user/orders',views.myOrders,name="myOrders"),
    path('user/addToCart',views.addToCart,name="addToCart"),
    path('user/removeFromCart',views.removeFromCart,name="removeFromCart"),
    path('user/viewDetails',views.viewDetails,name="viewDetails"),
    path('user/checkout',views.checkout,name="checkout"),
    path('user/placeOrder',views.placeOrder,name="placeOrder"),
    path('user/invoice',views.invoice,name="invoice"),
    path('user/emailUpdate',views.emailUpdate,name="emailUpdate"),
    path('user/otpVerification',views.otpVerification,name="otpVerification"),
    path('user/confirmUpdateEmail',views.confirmUpdateEmail,name="confirmUpdateEmail"),
    path('user/changeNumber',views.changeNumber,name="changeNumber"),
    path('user/grassCutterRegistration',views.grassCutterRegistration,name="grassCutterRegistration"),
    path('user/postJob',views.postJob,name="postJob"),
    path('user/ListJobs',views.listJobs,name="ListJobs"),
    path('user/grassCuttersList',views.grassCuttersList,name="grassCuttersList"),

    path('user/cancelOrder',views.cancelOrder,name="cancelOrder"),
    path('user/trackOrder',views.trackOrder,name="trackOrder"),
    path('user/selectCrop',views.selectCrop,name="selectCrop"),
    path('user/agroBasics',views.agroBasics,name="agroBasics"),
    path('user/viewBasic',views.viewBasic,name="viewBasic"),
    path('user/viewBasicDocument',views.viewBasicDocument,name="viewBasicDocument"),



    path('forgotPassword',views.forgotPassword,name='forgotPassword'),
    path('otp',views.otp,name='otp'),
    path('changePassword',views.changePassword,name='changePassword'),
    #path('productList',views.productList,name='productList')



]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)