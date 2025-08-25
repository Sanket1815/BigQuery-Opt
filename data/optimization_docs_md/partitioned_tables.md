<html lang="en" dir="ltr"><head><meta name="og-profile-acct" content="nadkarnisanket11@gmail.com">
    <meta name="google-signin-client-id" content="721724668570-nbkv1cfusk7kk4eni4pjvepaus73b13t.apps.googleusercontent.com">
    <meta name="google-signin-scope" content="profile email https://www.googleapis.com/auth/developerprofiles https://www.googleapis.com/auth/developerprofiles.award https://www.googleapis.com/auth/cloud-platform https://www.googleapis.com/auth/webhistory">
    <meta property="og:site_name" content="Google Cloud">
    <meta property="og:type" content="website"><meta name="theme-color" content="#039be5"><meta charset="utf-8">
    <meta content="IE=Edge" http-equiv="X-UA-Compatible">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    

    <link rel="manifest" href="/_pwa/cloud/manifest.json" crossorigin="use-credentials">
    <link rel="preconnect" href="//www.gstatic.com" crossorigin="">
    <link rel="preconnect" href="//fonts.gstatic.com" crossorigin="">
    <link rel="preconnect" href="//fonts.googleapis.com" crossorigin="">
    <link rel="preconnect" href="//apis.google.com" crossorigin="">
    <link rel="preconnect" href="//www.google-analytics.com" crossorigin=""><link rel="stylesheet" href="//fonts.googleapis.com/css?family=Google+Sans:400,500,700|Google+Sans+Text:400,400italic,500,500italic,700,700italic|Roboto:400,400italic,500,500italic,700,700italic|Roboto+Mono:400,500,700&amp;display=swap">
      <link rel="stylesheet" href="//fonts.googleapis.com/css2?family=Material+Icons&amp;family=Material+Symbols+Outlined&amp;display=block"><link rel="stylesheet" href="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/css/app.css">
      <link rel="shortcut icon" href="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/favicons/onecloud/favicon.ico">
    <link rel="apple-touch-icon" href="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/favicons/onecloud/super_cloud.png"><link rel="canonical" href="https://cloud.google.com/bigquery/docs/partitioned-tables"><link rel="search" type="application/opensearchdescription+xml" title="Google Cloud" href="https://cloud.google.com/s/opensearch.xml">
      <title>Introduction to partitioned tables &nbsp;|&nbsp; BigQuery &nbsp;|&nbsp; Google Cloud</title>

<meta property="og:title" content="Introduction to partitioned tables &nbsp;|&nbsp; BigQuery &nbsp;|&nbsp; Google Cloud"><meta name="description" content="Describes partitioned table in BigQuery, its types, limitations, quotas, pricing, and security.">
  <meta property="og:description" content="Describes partitioned table in BigQuery, its types, limitations, quotas, pricing, and security."><meta property="og:url" content="https://cloud.google.com/bigquery/docs/partitioned-tables"><meta property="og:image" content="https://cloud.google.com/_static/cloud/images/social-icon-google-cloud-1200-630.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630"><meta property="og:locale" content="en"><meta name="twitter:card" content="summary_large_image"><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtag/destination?id=AW-16541431319&amp;cx=c&amp;gtm=45je58d1v873759632za200zb897536842&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033763~105033765~105103161~105103163~105231383~105231385" nonce=""></script><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtag/destination?id=DC-2507573&amp;cx=c&amp;gtm=45je58d1v873759632za200zb897536842&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033763~105033765~105103161~105103163~105231383~105231385" nonce=""></script><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtag/destination?id=DC-7546819&amp;cx=c&amp;gtm=45je58d1v873759632za200zb897536842&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033763~105033765~105103161~105103163~105231383~105231385" nonce=""></script><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtag/destination?id=AW-10836211492&amp;cx=c&amp;gtm=45je58d1v873759632za200zb897536842&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033763~105033765~105103161~105103163~105231383~105231385" nonce=""></script><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtag/destination?id=AW-11082232239&amp;cx=c&amp;gtm=45je58d1v873759632za200zb897536842&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033763~105033765~105103161~105103163~105231383~105231385" nonce=""></script><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtag/js?id=G-WH2QY8WWF5&amp;cx=c&amp;gtm=45He58d1v897536842za200zb6343254&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033766~105033768~105103161~105103163~105231383~105231385" nonce=""></script><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtag/js?id=G-64EQFFKSHW&amp;l=atDataLayer&amp;cx=c&amp;gtm=45He58d1v9183356566za200&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033766~105033768~105103161~105103163~105231383~105231385" nonce=""></script><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtm.js?id=GTM-NS2VGJGH&amp;gtm=45He58d1v6343254za200&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033763~105033765~105091133~105103161~105103163~105231383~105231385" nonce=""></script><script type="text/javascript" async="" src="https://www.googletagmanager.com/gtm.js?id=GTM-M8NRS5J&amp;gtm=45He58d1v6343254za200&amp;tag_exp=101509157~103116026~103200004~103233427~104684208~104684211~105033763~105033765~105091133~105103161~105103163~105231383~105231385" nonce=""></script><script src="https://apis.google.com/_/scs/abc-static/_/js/k=gapi.gapi.en.GJa4oir6WlA.O/m=client/exm=gapi_iframes,googleapis_client/rt=j/sv=1/d=1/ed=1/rs=AHpOoo-oT18V72om9ubISB9Na8GvbQT5cg/cb=gapi.loaded_1?le=scs,fedcm_migration_mod" nonce="" async=""></script><script class="all-tenants" async="" src="//www.googletagmanager.com/gtm.js?id=GTM-NDV7K7V5&amp;l=atDataLayer" nonce=""></script><script async="" src="//www.googletagmanager.com/gtm.js?id=GTM-5CVQBG" nonce=""></script><script src="https://apis.google.com/_/scs/abc-static/_/js/k=gapi.gapi.en.GJa4oir6WlA.O/m=gapi_iframes,googleapis_client/rt=j/sv=1/d=1/ed=1/rs=AHpOoo-oT18V72om9ubISB9Na8GvbQT5cg/cb=gapi.loaded_0" nonce="" async=""></script><script src="https://apis.google.com/_/scs/abc-static/_/js/k=gapi.lb.en.PLtFj_-5DjQ.O/m=client/rt=j/sv=1/d=1/ed=1/rs=AHpOoo-J85zQk73PCqZPyWTydWEIq3_4KA/cb=gapi.loaded_0?le=scs" nonce="" async=""></script><script async="" src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/app_loader.js"></script><script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    
    "headline": "Introduction to partitioned tables"
  }
</script><script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [{
      "@type": "ListItem",
      "position": 1,
      "name": "BigQuery",
      "item": "https://cloud.google.com/bigquery"
    },{
      "@type": "ListItem",
      "position": 2,
      "name": "Documentation",
      "item": "https://cloud.google.com/bigquery/docs"
    },{
      "@type": "ListItem",
      "position": 3,
      "name": "Introduction to partitioned tables",
      "item": "https://cloud.google.com/bigquery/docs/partitioned-tables"
    }]
  }
  </script>
  <meta name="xsrf_token" content="niyMjdbgovuqlXmxLM8tklxtiFca1EUHAjkIvGUoRyE6MTc1NTM2MzczMTM0NTE2NA">
  

  <meta name="session_expiry" content="0">
  <meta name="uid" content="104443355188023252081">
  
    
    
    
    


































































































































































































  

  



























    









  




  





  




  




  




  
  
  
  







  
  
  
  











  







  







  








  






  



  


  


  


  

  





  


  

    
















































































  
    
  



























  
    
  

































































    
    
    
    


    
    
    
    

    
  

    
      <link rel="stylesheet" href="/extras.css"><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_app_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_app_custom_elements_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_header_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloudx_tabs_nav_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloud_shell_pane_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloudx_free_trial_eligible_store_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloudx_track_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_a11y_announce_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_analytics_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_badger_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_content_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_cookie_notification_bar_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_feature_tooltip_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_feedback_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_footer_linkboxes_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_footer_promos_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_footer_utility_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_hats_survey_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_heading_link_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_language_selector_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_notification_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_panel_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_progress_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_recommendations_sidebar_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_search_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_shell_activate_button_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_sitemask_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_snackbar_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_toc_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_tooltip_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_user_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloudx_experiments_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloudx_experiment_ids_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloudx_pricing_socket_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloudx_user_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_cloudx_utils_init_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_bookmark_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_book_nav_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_code_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_thumb_rating_module.js" nonce=""></script><script type="text/javascript" charset="UTF-8" src="https://www.gstatic.com/devops/connect/loader/tool_library.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_spinner_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_mwc_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_callout_notification_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_badge_awarded_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_dialog_module.js" nonce=""></script><script async="" src="https://www.gstatic.com/feedback/js/help/prod/service/lazy.min.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_fast_track_profile_creator_module.js" nonce=""></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_dropdown_list_module.js" nonce=""></script><script async="" defer="" src="https://www.gstatic.com/devops/connect/releases/devops-learning-tool-library_20250811_00_RC00/cloudshell/cloudshell.js" nonce=""></script><script type="text/javascript" charset="UTF-8" src="https://apis.google.com/js/client.js" nonce="" gapi_processed="true"></script><script src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/devsite_devsite_checkbox_module.js" nonce=""></script><style type="text/css">.gb_4d{font:13px/27px Roboto,Arial,sans-serif;z-index:986}@-webkit-keyframes gb__a{0%{opacity:0}50%{opacity:1}}@keyframes gb__a{0%{opacity:0}50%{opacity:1}}a.gb_Qa{border:none;color:#4285f4;cursor:default;font-weight:bold;outline:none;position:relative;text-align:center;text-decoration:none;text-transform:uppercase;white-space:nowrap;-webkit-user-select:none}a.gb_Qa:hover::after,a.gb_Qa:focus::after{background-color:rgba(0,0,0,.12);content:"";height:100%;left:0;position:absolute;top:0;width:100%}a.gb_Qa:hover,a.gb_Qa:focus{text-decoration:none}a.gb_Qa:active{background-color:rgba(153,153,153,.4);text-decoration:none}a.gb_Ra{background-color:#4285f4;color:#fff}a.gb_Ra:active{background-color:#0043b2}.gb_Sa{box-shadow:0 1px 1px rgba(0,0,0,.16)}.gb_Qa,.gb_Ra,.gb_Ta,.gb_Ua{display:inline-block;line-height:28px;padding:0 12px;border-radius:2px}.gb_Ta{background:#f8f8f8;border:1px solid #c6c6c6}.gb_Ua{background:#f8f8f8}.gb_Ta,#gb a.gb_Ta.gb_Ta,.gb_Ua{color:#666;cursor:default;text-decoration:none}#gb a.gb_Ua{cursor:default;text-decoration:none}.gb_Ua{border:1px solid #4285f4;font-weight:bold;outline:none;background:#4285f4;background:-webkit-gradient(linear,left top,left bottom,from(top),color-stop(#4387fd),to(#4683ea));background:-webkit-linear-gradient(top,#4387fd,#4683ea);background:linear-gradient(top,#4387fd,#4683ea);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#4387fd,endColorstr=#4683ea,GradientType=0)}#gb a.gb_Ua{color:#fff}.gb_Ua:hover{box-shadow:0 1px 0 rgba(0,0,0,.15)}.gb_Ua:active{box-shadow:inset 0 2px 0 rgba(0,0,0,.15);background:#3c78dc;background:-webkit-gradient(linear,left top,left bottom,from(top),color-stop(#3c7ae4),to(#3f76d3));background:-webkit-linear-gradient(top,#3c7ae4,#3f76d3);background:linear-gradient(top,#3c7ae4,#3f76d3);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#3c7ae4,endColorstr=#3f76d3,GradientType=0)}#gb .gb_Va{background:#fff;border:1px solid #dadce0;color:#1a73e8;display:inline-block;text-decoration:none}#gb .gb_Va:hover{background:#f8fbff;border-color:#dadce0;color:#174ea6}#gb .gb_Va:focus{background:#f4f8ff;color:#174ea6;outline:1px solid #174ea6}#gb .gb_Va:active,#gb .gb_Va:focus:active{background:#ecf3fe;color:#174ea6}#gb .gb_Va.gb_H{background:transparent;border:1px solid #5f6368;color:#8ab4f8;text-decoration:none}#gb .gb_Va.gb_H:hover{background:rgba(255,255,255,.04);color:#e8eaed}#gb .gb_Va.gb_H:focus{background:rgba(232,234,237,.12);color:#e8eaed;outline:1px solid #e8eaed}#gb .gb_Va.gb_H:active,#gb .gb_Va.gb_H:focus:active{background:rgba(232,234,237,.1);color:#e8eaed}.gb_dd{display:inline-block;vertical-align:middle}.gb_Qe .gb_Q{bottom:-3px;right:-5px}.gb_D{position:relative}.gb_B{display:inline-block;outline:none;vertical-align:middle;border-radius:2px;box-sizing:border-box;height:40px;width:40px;cursor:pointer;text-decoration:none}#gb#gb a.gb_B{cursor:pointer;text-decoration:none}.gb_B,a.gb_B{color:#000}.gb_ed{border-color:transparent;border-bottom-color:#fff;border-style:dashed dashed solid;border-width:0 8.5px 8.5px;display:none;position:absolute;left:11.5px;top:33px;z-index:1;height:0;width:0;-webkit-animation:gb__a .2s;animation:gb__a .2s}.gb_fd{border-color:transparent;border-style:dashed dashed solid;border-width:0 8.5px 8.5px;display:none;position:absolute;left:11.5px;z-index:1;height:0;width:0;-webkit-animation:gb__a .2s;animation:gb__a .2s;border-bottom-color:rgba(0,0,0,.2);top:32px}x:-o-prefocus,div.gb_fd{border-bottom-color:#ccc}.gb_la{background:#fff;border:1px solid #ccc;border-color:rgba(0,0,0,.2);color:#000;-webkit-box-shadow:0 2px 10px rgba(0,0,0,.2);box-shadow:0 2px 10px rgba(0,0,0,.2);display:none;outline:none;overflow:hidden;position:absolute;right:8px;top:62px;-webkit-animation:gb__a .2s;animation:gb__a .2s;border-radius:2px;-webkit-user-select:text}.gb_dd.gb_Uc .gb_ed,.gb_dd.gb_Uc .gb_fd,.gb_dd.gb_Uc .gb_la,.gb_Uc.gb_la{display:block}.gb_dd.gb_Uc.gb_gd .gb_ed,.gb_dd.gb_Uc.gb_gd .gb_fd{display:none}.gb_Re{position:absolute;right:8px;top:62px;z-index:-1}.gb_hd .gb_ed,.gb_hd .gb_fd,.gb_hd .gb_la{margin-top:-10px}.gb_dd:first-child,#gbsfw:first-child+.gb_dd{padding-left:4px}.gb_Fa.gb_Se .gb_dd:first-child{padding-left:0}.gb_Te{position:relative}.gb_3c .gb_Te,.gb_Kd .gb_Te{float:right}.gb_B{padding:8px;cursor:pointer}.gb_B::after{content:"";position:absolute;top:-4px;bottom:-4px;left:-4px;right:-4px}.gb_Fa .gb_id:not(.gb_Qa):focus img{background-color:rgba(0,0,0,.2);outline:none;-webkit-border-radius:50%;border-radius:50%}.gb_jd button svg,.gb_B{-webkit-border-radius:50%;border-radius:50%}.gb_jd button:focus:not(:focus-visible) svg,.gb_jd button:hover svg,.gb_jd button:active svg,.gb_B:focus:not(:focus-visible),.gb_B:hover,.gb_B:active,.gb_B[aria-expanded=true]{outline:none}.gb_Mc .gb_jd.gb_kd button:focus-visible svg,.gb_jd button:focus-visible svg,.gb_B:focus-visible{outline:1px solid #202124}.gb_Mc .gb_jd button:focus-visible svg,.gb_Mc .gb_B:focus-visible{outline:1px solid #f1f3f4}@media (forced-colors:active){.gb_Mc .gb_jd.gb_kd button:focus-visible svg,.gb_jd button:focus-visible svg,.gb_Mc .gb_jd button:focus-visible svg{outline:1px solid currentcolor}}.gb_Mc .gb_jd.gb_kd button:focus svg,.gb_Mc .gb_jd.gb_kd button:focus:hover svg,.gb_jd button:focus svg,.gb_jd button:focus:hover svg,.gb_B:focus,.gb_B:focus:hover{background-color:rgba(60,64,67,.1)}.gb_Mc .gb_jd.gb_kd button:active svg,.gb_jd button:active svg,.gb_B:active{background-color:rgba(60,64,67,.12)}.gb_Mc .gb_jd.gb_kd button:hover svg,.gb_jd button:hover svg,.gb_B:hover{background-color:rgba(60,64,67,.08)}.gb_Wa .gb_B.gb_Za:hover{background-color:transparent}.gb_B[aria-expanded=true],.gb_B:hover[aria-expanded=true]{background-color:rgba(95,99,104,.24)}.gb_B[aria-expanded=true] .gb_F{fill:#5f6368;opacity:1}.gb_Mc .gb_jd button:hover svg,.gb_Mc .gb_B:hover{background-color:rgba(232,234,237,.08)}.gb_Mc .gb_jd button:focus svg,.gb_Mc .gb_jd button:focus:hover svg,.gb_Mc .gb_B:focus,.gb_Mc .gb_B:focus:hover{background-color:rgba(232,234,237,.1)}.gb_Mc .gb_jd button:active svg,.gb_Mc .gb_B:active{background-color:rgba(232,234,237,.12)}.gb_Mc .gb_B[aria-expanded=true],.gb_Mc .gb_B:hover[aria-expanded=true]{background-color:rgba(255,255,255,.12)}.gb_Mc .gb_B[aria-expanded=true] .gb_F{fill:#fff;opacity:1}.gb_dd{padding:4px}.gb_Fa.gb_Se .gb_dd{padding:4px 2px}.gb_Fa.gb_Se .gb_z.gb_dd{padding-left:6px}.gb_la{z-index:991;line-height:normal}.gb_la.gb_ld{left:0;right:auto}@media (max-width:350px){.gb_la.gb_ld{left:0}}.gb_Ue .gb_la{top:56px}.gb_R{display:none!important}.gb_od{visibility:hidden}.gb_J .gb_B,.gb_ka .gb_J .gb_B{background-position:-64px -29px}.gb_1 .gb_J .gb_B{background-position:-29px -29px;opacity:1}.gb_J .gb_B,.gb_J .gb_B:hover,.gb_J .gb_B:focus{opacity:1}.gb_L{display:none}@media screen and (max-width:319px){.gb_md:not(.gb_nd) .gb_J{display:none;visibility:hidden}}.gb_Q{display:none}.gb_ad{font-family:Google Sans,Roboto,Helvetica,Arial,sans-serif;font-size:20px;font-weight:400;letter-spacing:0.25px;line-height:48px;margin-bottom:2px;opacity:1;overflow:hidden;padding-left:16px;position:relative;text-overflow:ellipsis;vertical-align:middle;top:2px;white-space:nowrap;-webkit-flex:1 1 auto;-webkit-box-flex:1;flex:1 1 auto}.gb_ad.gb_bd{color:#3c4043}.gb_Fa.gb_cc .gb_ad{margin-bottom:0}.gb_td.gb_vd .gb_ad{padding-left:4px}.gb_Fa.gb_cc .gb_wd{position:relative;top:-2px}.gb_cd{display:none}.gb_Fa{color:black;min-width:160px;position:relative;-webkit-transition:box-shadow 250ms;transition:box-shadow 250ms}.gb_Fa.gb_Tc{min-width:120px}.gb_Fa.gb_xd .gb_yd{display:none}.gb_Fa.gb_xd .gb_md{height:56px}header.gb_Fa{display:block}.gb_Fa svg{fill:currentColor}.gb_Ed{position:fixed;top:0;width:100%}.gb_zd{-webkit-box-shadow:0 4px 5px 0 rgba(0,0,0,.14),0 1px 10px 0 rgba(0,0,0,.12),0 2px 4px -1px rgba(0,0,0,.2);box-shadow:0 4px 5px 0 rgba(0,0,0,.14),0 1px 10px 0 rgba(0,0,0,.12),0 2px 4px -1px rgba(0,0,0,.2)}.gb_Fd{height:64px}.gb_md{-webkit-box-sizing:border-box;box-sizing:border-box;position:relative;width:100%;display:-webkit-box;display:-webkit-flex;display:flex;-webkit-box-pack:space-between;-webkit-justify-content:space-between;justify-content:space-between;min-width:-webkit-min-content;min-width:min-content}.gb_Fa:not(.gb_cc) .gb_md{padding:8px}.gb_Fa.gb_Hd .gb_md{-webkit-flex:1 0 auto;-webkit-box-flex:1;flex:1 0 auto}.gb_Fa .gb_md.gb_nd.gb_Id{min-width:0}.gb_Fa.gb_cc .gb_md{padding:4px;padding-left:8px;min-width:0}.gb_yd{height:48px;vertical-align:middle;white-space:nowrap;-webkit-box-align:center;-webkit-align-items:center;align-items:center;display:-webkit-box;display:-webkit-flex;display:flex;-webkit-user-select:none}.gb_Bd>.gb_yd{display:table-cell;width:100%}.gb_td{padding-right:30px;box-sizing:border-box;-webkit-flex:1 0 auto;-webkit-box-flex:1;flex:1 0 auto}.gb_Fa.gb_cc .gb_td{padding-right:14px}.gb_Cd{-webkit-flex:1 1 100%;-webkit-box-flex:1;flex:1 1 100%}.gb_Cd>:only-child{display:inline-block}.gb_Dd.gb_4c{padding-left:4px}.gb_Dd.gb_Jd,.gb_Fa.gb_Hd .gb_Dd,.gb_Fa.gb_cc:not(.gb_Kd) .gb_Dd{padding-left:0}.gb_Fa.gb_cc .gb_Dd.gb_Jd{padding-right:0}.gb_Fa.gb_cc .gb_Dd.gb_Jd .gb_Wa{margin-left:10px}.gb_4c{display:inline}.gb_Fa.gb_Xc .gb_Dd.gb_Ld,.gb_Fa.gb_Kd .gb_Dd.gb_Ld{padding-left:2px}.gb_ad{display:inline-block}.gb_Dd{-webkit-box-sizing:border-box;box-sizing:border-box;height:48px;line-height:normal;padding:0 4px;padding-left:30px;-webkit-flex:0 0 auto;-webkit-box-flex:0;flex:0 0 auto;-webkit-box-pack:flex-end;-webkit-justify-content:flex-end;justify-content:flex-end}.gb_Kd{height:48px}.gb_Fa.gb_Kd{min-width:auto}.gb_Kd .gb_Dd{float:right;padding-left:32px}.gb_Kd .gb_Dd.gb_Md{padding-left:0}.gb_Nd{font-size:14px;max-width:200px;overflow:hidden;padding:0 12px;text-overflow:ellipsis;white-space:nowrap;-webkit-user-select:text}.gb_qd{-webkit-transition:background-color .4s;-webkit-transition:background-color .4s;transition:background-color .4s}.gb_Od{color:black}.gb_Mc{color:white}.gb_Fa a,.gb_Qc a{color:inherit}.gb_ba{color:rgba(0,0,0,.87)}.gb_Fa svg,.gb_Qc svg,.gb_td .gb_ud,.gb_3c .gb_ud{color:#5f6368;opacity:1}.gb_Mc svg,.gb_Qc.gb_Vc svg,.gb_Mc .gb_td .gb_ud,.gb_Mc .gb_td .gb_Lc,.gb_Mc .gb_td .gb_wd,.gb_Qc.gb_Vc .gb_ud{color:rgba(255,255,255,.87)}.gb_Mc .gb_td .gb_Pd:not(.gb_Qd){opacity:.87}.gb_bd{color:inherit;opacity:1;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased}.gb_Mc .gb_bd,.gb_Od .gb_bd{opacity:1}.gb_Rd{position:relative}.gb_M{font-family:arial,sans-serif;line-height:normal;padding-right:15px}a.gb_X,span.gb_X{color:rgba(0,0,0,.87);text-decoration:none}.gb_Mc a.gb_X,.gb_Mc span.gb_X{color:white}a.gb_X:focus{outline-offset:2px}a.gb_X:hover{text-decoration:underline}.gb_Z{display:inline-block;padding-left:15px}.gb_Z .gb_X{display:inline-block;line-height:24px;vertical-align:middle}.gb_rd{font-family:Google Sans,Roboto,Helvetica,Arial,sans-serif;font-weight:500;font-size:14px;letter-spacing:.25px;line-height:16px;margin-left:10px;margin-right:8px;min-width:96px;padding:9px 23px;text-align:center;vertical-align:middle;border-radius:4px;box-sizing:border-box}.gb_Fa.gb_Kd .gb_rd{margin-left:8px}#gb a.gb_Ua.gb_rd{cursor:pointer}.gb_Ua.gb_rd:hover{background:#1b66c9;-webkit-box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3);box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3)}.gb_Ua.gb_rd:focus,.gb_Ua.gb_rd:hover:focus{background:#1c5fba;-webkit-box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3);box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3)}.gb_Ua.gb_rd:active{background:#1b63c1;-webkit-box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3);box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3)}.gb_rd{background:#1a73e8;border:1px solid transparent}.gb_Fa.gb_cc .gb_rd{padding:9px 15px;min-width:80px}.gb_Sd{text-align:left}#gb .gb_Mc a.gb_rd:not(.gb_H),#gb.gb_Mc a.gb_rd{background:#fff;border-color:#dadce0;-webkit-box-shadow:none;box-shadow:none;color:#1a73e8}#gb a.gb_Ua.gb_H.gb_rd{background:#8ab4f8;border:1px solid transparent;-webkit-box-shadow:none;box-shadow:none;color:#202124}#gb .gb_Mc a.gb_rd:hover:not(.gb_H),#gb.gb_Mc a.gb_rd:hover{background:#f8fbff;border-color:#cce0fc}#gb a.gb_Ua.gb_H.gb_rd:hover{background:#93baf9;border-color:transparent;-webkit-box-shadow:0 1px 3px 1px rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.3);box-shadow:0 1px 3px 1px rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.3)}#gb .gb_Mc a.gb_rd:focus:not(.gb_H),#gb .gb_Mc a.gb_rd:focus:hover:not(.gb_H),#gb.gb_Mc a.gb_rd:focus:not(.gb_H),#gb.gb_Mc a.gb_rd:focus:hover:not(.gb_H){background:#f4f8ff;outline:1px solid #c9ddfc}#gb a.gb_Ua.gb_H.gb_rd:focus,#gb a.gb_Ua.gb_H.gb_rd:focus:hover{background:#a6c6fa;border-color:transparent;-webkit-box-shadow:none;box-shadow:none}#gb .gb_Mc a.gb_rd:active:not(.gb_H),#gb.gb_Mc a.gb_rd:active{background:#ecf3fe}#gb a.gb_Ua.gb_H.gb_rd:active{background:#a1c3f9;-webkit-box-shadow:0 1px 2px rgba(60,64,67,.3),0 2px 6px 2px rgba(60,64,67,.15);box-shadow:0 1px 2px rgba(60,64,67,.3),0 2px 6px 2px rgba(60,64,67,.15)}.gb_K{display:none}@media screen and (max-width:319px){.gb_md .gb_J{display:none;visibility:hidden}}.gb_Wa{background-color:rgba(255,255,255,.88);border:1px solid #dadce0;-webkit-box-sizing:border-box;box-sizing:border-box;cursor:pointer;display:inline-block;max-height:48px;overflow:hidden;outline:none;padding:0;vertical-align:middle;width:134px;-webkit-border-radius:8px;border-radius:8px}.gb_Wa.gb_H{background-color:transparent;border:1px solid #5f6368}.gb_3a{display:inherit}.gb_Wa.gb_H .gb_3a{background:#fff;-webkit-border-radius:4px;border-radius:4px;display:inline-block;left:8px;margin-right:5px;position:relative;padding:3px;top:-1px}.gb_Wa:hover{border:1px solid #d2e3fc;background-color:rgba(248,250,255,.88)}.gb_Wa.gb_H:hover{background-color:rgba(241,243,244,.04);border:1px solid #5f6368}.gb_Wa:focus-visible,.gb_Wa:focus{background-color:#fff;outline:1px solid #202124;-webkit-box-shadow:0 1px 2px 0 rgba(60,64,67,.3),0 1px 3px 1px rgba(60,64,67,.15);box-shadow:0 1px 2px 0 rgba(60,64,67,.3),0 1px 3px 1px rgba(60,64,67,.15)}.gb_Wa.gb_H:focus-visible,.gb_Wa.gb_H:focus{background-color:rgba(241,243,244,.12);outline:1px solid #f1f3f4;-webkit-box-shadow:0 1px 3px 1px rgba(0,0,0,.15),0 1px 2px 0 rgba(0,0,0,.3);box-shadow:0 1px 3px 1px rgba(0,0,0,.15),0 1px 2px 0 rgba(0,0,0,.3)}.gb_Wa.gb_H:active,.gb_Wa.gb_Uc.gb_H:focus{background-color:rgba(241,243,244,.1);border:1px solid #5f6368}.gb_4a{display:inline-block;padding-bottom:2px;padding-left:7px;padding-top:2px;text-align:center;vertical-align:middle;line-height:32px;width:78px}.gb_Wa.gb_H .gb_4a{line-height:26px;margin-left:0;padding-bottom:0;padding-left:0;padding-top:0;width:72px}.gb_4a.gb_5a{background-color:#f1f3f4;-webkit-border-radius:4px;border-radius:4px;margin-left:8px;padding-left:0;line-height:30px}.gb_4a.gb_5a .gb_Jc{vertical-align:middle}.gb_Fa:not(.gb_cc) .gb_Wa{margin-left:10px;margin-right:4px}.gb_Td{max-height:32px;width:78px}.gb_Wa.gb_H .gb_Td{max-height:26px;width:72px}.gb_P{-webkit-background-size:32px 32px;background-size:32px 32px;border:0;-webkit-border-radius:50%;border-radius:50%;display:block;margin:0px;position:relative;height:32px;width:32px;z-index:0}.gb_eb{background-color:#e8f0fe;border:1px solid rgba(32,33,36,.08);position:relative}.gb_eb.gb_P{height:30px;width:30px}.gb_eb.gb_P:hover,.gb_eb.gb_P:active{-webkit-box-shadow:none;box-shadow:none}.gb_fb{background:#fff;border:none;-webkit-border-radius:50%;border-radius:50%;bottom:2px;-webkit-box-shadow:0px 1px 2px 0px rgba(60,64,67,.30),0px 1px 3px 1px rgba(60,64,67,.15);box-shadow:0px 1px 2px 0px rgba(60,64,67,.30),0px 1px 3px 1px rgba(60,64,67,.15);height:14px;margin:2px;position:absolute;right:0;width:14px}.gb_wc{color:#1f71e7;font:400 22px/32px Google Sans,Roboto,Helvetica,Arial,sans-serif;text-align:center;text-transform:uppercase}@media (-webkit-min-device-pixel-ratio:1.25),(min-resolution:1.25dppx),(min-device-pixel-ratio:1.25){.gb_P::before,.gb_gb::before{display:inline-block;-webkit-transform:scale(0.5);-webkit-transform:scale(0.5);transform:scale(0.5);-webkit-transform-origin:left 0;-webkit-transform-origin:left 0;transform-origin:left 0}.gb_3 .gb_gb::before{-webkit-transform:scale(scale(0.416666667));-webkit-transform:scale(scale(0.416666667));transform:scale(scale(0.416666667))}}.gb_P:hover,.gb_P:focus{-webkit-box-shadow:0 1px 0 rgba(0,0,0,.15);box-shadow:0 1px 0 rgba(0,0,0,.15)}.gb_P:active{-webkit-box-shadow:inset 0 2px 0 rgba(0,0,0,.15);box-shadow:inset 0 2px 0 rgba(0,0,0,.15)}.gb_P:active::after{background:rgba(0,0,0,.1);-webkit-border-radius:50%;border-radius:50%;content:"";display:block;height:100%}.gb_hb{cursor:pointer;line-height:40px;min-width:30px;opacity:.75;overflow:hidden;vertical-align:middle;text-overflow:ellipsis}.gb_B.gb_hb{width:auto}.gb_hb:hover,.gb_hb:focus{opacity:.85}.gb_hd .gb_hb,.gb_hd .gb_Wd{line-height:26px}#gb#gb.gb_hd a.gb_hb,.gb_hd .gb_Wd{font-size:11px;height:auto}.gb_ib{border-top:4px solid #000;border-left:4px dashed transparent;border-right:4px dashed transparent;display:inline-block;margin-left:6px;opacity:.75;vertical-align:middle}.gb_Za:hover .gb_ib{opacity:.85}.gb_Wa>.gb_z{padding:3px 3px 3px 4px}.gb_Xd.gb_od{color:#fff}.gb_1 .gb_hb,.gb_1 .gb_ib{opacity:1}#gb#gb.gb_1.gb_1 a.gb_hb,#gb#gb .gb_1.gb_1 a.gb_hb{color:#fff}.gb_1.gb_1 .gb_ib{border-top-color:#fff;opacity:1}.gb_ka .gb_P:hover,.gb_1 .gb_P:hover,.gb_ka .gb_P:focus,.gb_1 .gb_P:focus{-webkit-box-shadow:0 1px 0 rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.2);box-shadow:0 1px 0 rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.2)}.gb_Zd .gb_z,.gb_0d .gb_z{position:absolute;right:1px}.gb_z.gb_0,.gb_jb.gb_0,.gb_Za.gb_0{-webkit-flex:0 1 auto;-webkit-box-flex:0;flex:0 1 auto}.gb_1d.gb_2d .gb_hb{width:30px!important}.gb_3d{height:40px;position:absolute;right:-5px;top:-5px;width:40px}.gb_4d .gb_3d,.gb_5d .gb_3d{right:0;top:0}.gb_z .gb_B{padding:4px}.gb_S{display:none}sentinel{}</style><script id="ogb-head-script">;this.gbar_={CONFIG:[[[0,"www.gstatic.com","og.qtm.en_US.v2pk7dVghog.2019.O","com","en","331",0,[4,2,"","","","793424555","0"],null,"lLmgaI-AGfmG-LYPyLSZuQM",null,0,"og.qtm.5bOMfS7uCn8.L.W.O","AA2YrTthfa-GW6nWNiVo32au3OStcP0_zg","AA2YrTs5z5IeveM3_8fj3UK_0H1gj7fqJg","",2,1,200,"USA",null,null,"18","331",1,null,null,111881503,null,0,0],null,[1,0.1000000014901161,2,1],null,[1,0,0,null,"0","nadkarnisanket11@gmail.com","","AIhRldIzA5lX0DdIADrbvU2spPh9rszVVZ6EP4uHPSpGyErOau_sk4bpfhrWVBpm21CbruhqVb1d9Lc-pxQUaFoQjVVCyAoFyw",0,0,0,""],[0,0,"",1,0,0,0,0,0,0,null,0,0,null,0,0,null,null,0,0,0,"","","","","","",null,0,0,0,0,0,null,null,null,"rgba(32,33,36,1)","rgba(255,255,255,1)",0,0,0,null,null,null,0],["%1$s (default)","Brand account",1,"%1$s (delegated)",1,null,83,"?authuser=$authuser",null,null,null,1,"https://accounts.google.com/ListAccounts?listPages=0\u0026authuser=0\u0026pid=331\u0026gpsia=1\u0026source=ogb\u0026atic=1\u0026mo=1\u0026mn=1\u0026hl=en",0,"dashboard",null,null,null,null,"Profile","",1,null,"Signed out","https://accounts.google.com/AccountChooser?source=ogb\u0026continue=$continue\u0026Email=$email\u0026ec=GAhAywI","https://accounts.google.com/RemoveLocalAccount?source=ogb","Remove","Sign in",0,1,1,0,1,1,0,null,null,null,"Session expired",null,null,null,"Visitor",null,"Default","Delegated","Sign out of all accounts",1,null,null,0,null,null,"myaccount.google.com","https",0,1,0],null,["1","gci_91f30755d6a6b787dcc2a4062e6e9824.js","googleapis.client:gapi.iframes","0","en"],null,null,null,null,["m;/_/scs/abc-static/_/js/k=gapi.gapi.en.GJa4oir6WlA.O/d=1/rs=AHpOoo-oT18V72om9ubISB9Na8GvbQT5cg/m=__features__","https://apis.google.com","","","1","",null,1,"es_plusone_gc_20250803.0_p0","en",null,0],[0.009999999776482582,"com","331",[null,"","0",null,1,5184000,null,null,"",null,null,null,null,null,0,null,0,null,1,0,0,0,null,null,0,0,null,0,0,0,0,0],null,null,null,0],[1,null,null,40400,331,"USA","en","793424555.0",8,null,1,0,null,null,null,null,"3700949,105071010,105071012",null,null,null,"lLmgaI-AGfmG-LYPyLSZuQM",0,0,0,null,2,5,"nn",39,0,0,null,null,1,111881503,0,0],[[null,null,null,"https://www.gstatic.com/og/_/js/k=og.qtm.en_US.v2pk7dVghog.2019.O/rt=j/m=qabr,qgl,q_dnp,qcwid,qbd,qapid,qads,qrcd,q_dg/exm=qaaw,qadd,qaid,qein,qhaw,qhba,qhbr,qhch,qhga,qhid,qhin/d=1/ed=1/rs=AA2YrTthfa-GW6nWNiVo32au3OStcP0_zg"],[null,null,null,"https://www.gstatic.com/og/_/ss/k=og.qtm.5bOMfS7uCn8.L.W.O/m=qcwid,qba/excm=qaaw,qadd,qaid,qein,qhaw,qhba,qhbr,qhch,qhga,qhid,qhin/d=1/ed=1/ct=zgms/rs=AA2YrTs5z5IeveM3_8fj3UK_0H1gj7fqJg"]],null,null,null,[[[null,null,[null,null,null,"https://ogs.google.com/u/0/widget/account?amb=1"],0,414,436,57,4,1,0,0,65,66,8000,"https://accounts.google.com/SignOutOptions?hl=en\u0026continue=https://cloud.google.com/_d/profile/ogb\u0026ec=GBRAywI",68,2,null,null,1,113,"Something went wrong.%1$s Refresh to try again or %2$schoose another account%3$s.",3,null,null,75,0,null,null,null,null,null,null,null,"/widget/account",["https","myaccount.google.com",0,32,83,0],0,0,1,["Critical security alert","Important account alert","Storage usage alert",null,1,0],0,1,null,1,1,null,null,null,null,0,0,0,null,0,0,null,null,null,null,null,null,null,null,null,0],[null,null,[null,null,null,"https://ogs.google.com/u/0/widget/callout/sid?dc=1"],null,280,420,70,25,0,null,0,null,null,8000,null,71,4,null,null,null,null,null,null,null,null,76,null,null,null,107,108,109,"",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,0]],null,null,"18","331",1,0,null,"en",0,["?authuser=$authuser","https://accounts.google.com/AddSession?continue=\u0026ec=GAlAywI","https://accounts.google.com/Logout?continue=https://cloud.google.com/\u0026service=ahsid\u0026ec=GAdAywI","https://accounts.google.com/ListAccounts?listPages=0\u0026authuser=0\u0026pid=331\u0026gpsia=1\u0026source=ogb\u0026atic=1\u0026mo=1\u0026mn=1\u0026hl=en",0,0,"",0,0,null,0,0,"https://accounts.google.com/ServiceLogin?continue=https://cloud.google.com/\u0026authuser=0\u0026ec=GAZAywI",null,null,0,null,null,null,0],0,0,0,[null,"",null,null,null,1,null,0,0,"","","","https://ogads-pa.clients6.google.com",0,0,0,"","",0,0,null,86400,null,1,null,null,0,null,0,0,"8559284470",0,0,0],0,null,null,null,1,0,"nadkarnisanket11@gmail.com",0],null,[["mousedown","touchstart","touchmove","wheel","keydown"],300000],[[null,null,null,"https://accounts.google.com/RotateCookiesPage"],3,null,null,null,0,1]]],};this.gbar_=this.gbar_||{};(function(_){var window=this;
try{
_._F_toggles_initialize=function(a){(typeof globalThis!=="undefined"?globalThis:typeof self!=="undefined"?self:this)._F_toggles_gbar_=a||[]};(0,_._F_toggles_initialize)([]);
/*

 Copyright The Closure Library Authors.
 SPDX-License-Identifier: Apache-2.0
*/
var ja,pa,qa,ua,wa,xa,Fa,Ga,$a,cb,eb,jb,fb,lb,rb,Db,Eb,Fb,Gb;_.aa=function(a,b){if(Error.captureStackTrace)Error.captureStackTrace(this,_.aa);else{const c=Error().stack;c&&(this.stack=c)}a&&(this.message=String(a));b!==void 0&&(this.cause=b)};_.ba=function(a){a.zk=!0;return a};_.ia=function(a){var b=a;if(da(b)){if(!/^\s*(?:-?[1-9]\d*|0)?\s*$/.test(b))throw Error(String(b));}else if(ea(b)&&!Number.isSafeInteger(b))throw Error(String(b));return fa?BigInt(a):a=ha(a)?a?"1":"0":da(a)?a.trim()||"0":String(a)};
ja=function(a,b){if(a.length>b.length)return!1;if(a.length<b.length||a===b)return!0;for(let c=0;c<a.length;c++){const d=a[c],e=b[c];if(d>e)return!1;if(d<e)return!0}};_.ka=function(a){_.t.setTimeout(()=>{throw a;},0)};_.ma=function(){return _.la().toLowerCase().indexOf("webkit")!=-1};_.la=function(){var a=_.t.navigator;return a&&(a=a.userAgent)?a:""};pa=function(a){if(!na||!oa)return!1;for(let b=0;b<oa.brands.length;b++){const {brand:c}=oa.brands[b];if(c&&c.indexOf(a)!=-1)return!0}return!1};
_.u=function(a){return _.la().indexOf(a)!=-1};qa=function(){return na?!!oa&&oa.brands.length>0:!1};_.ra=function(){return qa()?!1:_.u("Opera")};_.sa=function(){return qa()?!1:_.u("Trident")||_.u("MSIE")};_.ta=function(){return _.u("Firefox")||_.u("FxiOS")};_.va=function(){return _.u("Safari")&&!(ua()||(qa()?0:_.u("Coast"))||_.ra()||(qa()?0:_.u("Edge"))||(qa()?pa("Microsoft Edge"):_.u("Edg/"))||(qa()?pa("Opera"):_.u("OPR"))||_.ta()||_.u("Silk")||_.u("Android"))};
ua=function(){return qa()?pa("Chromium"):(_.u("Chrome")||_.u("CriOS"))&&!(qa()?0:_.u("Edge"))||_.u("Silk")};wa=function(){return na?!!oa&&!!oa.platform:!1};xa=function(){return _.u("iPhone")&&!_.u("iPod")&&!_.u("iPad")};_.ya=function(){return xa()||_.u("iPad")||_.u("iPod")};_.za=function(){return wa()?oa.platform==="macOS":_.u("Macintosh")};_.Ba=function(a,b){return _.Aa(a,b)>=0};_.Ca=function(a,b=!1){return b&&Symbol.for&&a?Symbol.for(a):a!=null?Symbol(a):Symbol()};
_.Ea=function(a,b){return b===void 0?a.j!==Da&&!!(2&(a.fa[_.v]|0)):!!(2&b)&&a.j!==Da};Fa=function(a){return a};Ga=function(a,b){a.__closure__error__context__984382||(a.__closure__error__context__984382={});a.__closure__error__context__984382.severity=b};_.Ha=function(a){a=Error(a);Ga(a,"warning");return a};_.Ja=function(a,b){if(a!=null){var c;var d=(c=Ia)!=null?c:Ia={};c=d[a]||0;c>=b||(d[a]=c+1,a=Error(),Ga(a,"incident"),_.ka(a))}};
_.La=function(a){if(typeof a!=="boolean")throw Error("k`"+_.Ka(a)+"`"+a);return a};_.Ma=function(a){if(a==null||typeof a==="boolean")return a;if(typeof a==="number")return!!a};_.Oa=function(a){if(!(0,_.Na)(a))throw _.Ha("enum");return a|0};_.Pa=function(a){return a==null?a:(0,_.Na)(a)?a|0:void 0};_.Qa=function(a){if(typeof a!=="number")throw _.Ha("int32");if(!(0,_.Na)(a))throw _.Ha("int32");return a|0};_.Ra=function(a){if(a!=null&&typeof a!=="string")throw Error();return a};
_.Sa=function(a){return a==null||typeof a==="string"?a:void 0};_.Va=function(a,b,c){if(a!=null&&a[_.Ta]===_.Ua)return a;if(Array.isArray(a)){var d=a[_.v]|0;c=d|c&32|c&2;c!==d&&(a[_.v]=c);return new b(a)}};_.Ya=function(a){const b=_.Wa(_.Xa);return b?a[b]:void 0};$a=function(a,b){b<100||_.Ja(Za,1)};
cb=function(a,b,c,d){const e=d!==void 0;d=!!d;var f=_.Wa(_.Xa),g;!e&&f&&(g=a[f])&&g.xd($a);f=[];var h=a.length;let k;g=4294967295;let l=!1;const m=!!(b&64),p=m?b&128?0:-1:void 0;if(!(b&1||(k=h&&a[h-1],k!=null&&typeof k==="object"&&k.constructor===Object?(h--,g=h):k=void 0,!m||b&128||e))){l=!0;var r;g=((r=ab)!=null?r:Fa)(g-p,p,a,k,void 0)+p}b=void 0;for(r=0;r<h;r++){let w=a[r];if(w!=null&&(w=c(w,d))!=null)if(m&&r>=g){const D=r-p;var q=void 0;((q=b)!=null?q:b={})[D]=w}else f[r]=w}if(k)for(let w in k){q=
k[w];if(q==null||(q=c(q,d))==null)continue;h=+w;let D;if(m&&!Number.isNaN(h)&&(D=h+p)<g)f[D]=q;else{let Q;((Q=b)!=null?Q:b={})[w]=q}}b&&(l?f.push(b):f[g]=b);e&&_.Wa(_.Xa)&&(a=_.Ya(a))&&"function"==typeof _.bb&&a instanceof _.bb&&(f[_.Xa]=a.i());return f};
eb=function(a){switch(typeof a){case "number":return Number.isFinite(a)?a:""+a;case "bigint":return(0,_.db)(a)?Number(a):""+a;case "boolean":return a?1:0;case "object":if(Array.isArray(a)){const b=a[_.v]|0;return a.length===0&&b&1?void 0:cb(a,b,eb)}if(a!=null&&a[_.Ta]===_.Ua)return fb(a);if("function"==typeof _.gb&&a instanceof _.gb)return a.j();return}return a};jb=function(a,b){if(b){ab=b==null||b===Fa||b[hb]!==ib?Fa:b;try{return fb(a)}finally{ab=void 0}}return fb(a)};
fb=function(a){a=a.fa;return cb(a,a[_.v]|0,eb)};
_.mb=function(a,b,c,d=0){if(a==null){var e=32;c?(a=[c],e|=128):a=[];b&&(e=e&-8380417|(b&1023)<<13)}else{if(!Array.isArray(a))throw Error("l");e=a[_.v]|0;if(kb&&1&e)throw Error("m");2048&e&&!(2&e)&&lb();if(e&256)throw Error("n");if(e&64)return d!==0||e&2048||(a[_.v]=e|2048),a;if(c&&(e|=128,c!==a[0]))throw Error("o");a:{c=a;e|=64;var f=c.length;if(f){var g=f-1;const k=c[g];if(k!=null&&typeof k==="object"&&k.constructor===Object){b=e&128?0:-1;g-=b;if(g>=1024)throw Error("q");for(var h in k)if(f=+h,f<
g)c[f+b]=k[h],delete k[h];else break;e=e&-8380417|(g&1023)<<13;break a}}if(b){h=Math.max(b,f-(e&128?0:-1));if(h>1024)throw Error("r");e=e&-8380417|(h&1023)<<13}}}e|=64;d===0&&(e|=2048);a[_.v]=e;return a};lb=function(){if(kb)throw Error("p");_.Ja(nb,5)};
rb=function(a,b){if(typeof a!=="object")return a;if(Array.isArray(a)){var c=a[_.v]|0;a.length===0&&c&1?a=void 0:c&2||(!b||4096&c||16&c?a=_.ob(a,c,!1,b&&!(c&16)):(a[_.v]|=34,c&4&&Object.freeze(a)));return a}if(a!=null&&a[_.Ta]===_.Ua)return b=a.fa,c=b[_.v]|0,_.Ea(a,c)?a:_.pb(a,b,c)?_.qb(a,b):_.ob(b,c);if("function"==typeof _.gb&&a instanceof _.gb)return a};_.qb=function(a,b,c){a=new a.constructor(b);c&&(a.j=Da);a.o=Da;return a};
_.ob=function(a,b,c,d){d!=null||(d=!!(34&b));a=cb(a,b,rb,d);d=32;c&&(d|=2);b=b&8380609|d;a[_.v]=b;return a};_.tb=function(a){const b=a.fa,c=b[_.v]|0;return _.Ea(a,c)?_.pb(a,b,c)?_.qb(a,b,!0):new a.constructor(_.ob(b,c,!1)):a};_.ub=function(a){if(a.j!==Da)return!1;var b=a.fa;b=_.ob(b,b[_.v]|0);b[_.v]|=2048;a.fa=b;a.j=void 0;a.o=void 0;return!0};_.vb=function(a){if(!_.ub(a)&&_.Ea(a,a.fa[_.v]|0))throw Error();};_.wb=function(a,b){b===void 0&&(b=a[_.v]|0);b&32&&!(b&4096)&&(a[_.v]=b|4096)};
_.pb=function(a,b,c){return c&2?!0:c&32&&!(c&4096)?(b[_.v]=c|2,a.j=Da,!0):!1};_.xb=function(a,b,c,d,e){const f=c+(e?0:-1);var g=a.length-1;if(g>=1+(e?0:-1)&&f>=g){const h=a[g];if(h!=null&&typeof h==="object"&&h.constructor===Object)return h[c]=d,b}if(f<=g)return a[f]=d,b;if(d!==void 0){let h;g=((h=b)!=null?h:b=a[_.v]|0)>>13&1023||536870912;c>=g?d!=null&&(a[g+(e?0:-1)]={[c]:d}):a[f]=d}return b};
_.zb=function(a,b,c,d,e){let f=!1;d=_.yb(a,d,e,g=>{const h=_.Va(g,c,b);f=h!==g&&h!=null;return h});if(d!=null)return f&&!_.Ea(d)&&_.wb(a,b),d};_.Ab=function(){const a=class{constructor(){throw Error();}};Object.setPrototypeOf(a,a.prototype);return a};_.x=function(a,b){return a!=null?!!a:!!b};_.y=function(a,b){b==void 0&&(b="");return a!=null?a:b};_.Bb=function(a,b,c){for(const d in a)b.call(c,a[d],d,a)};_.Cb=function(a){for(const b in a)return!1;return!0};Db=Object.defineProperty;
Eb=function(a){a=["object"==typeof globalThis&&globalThis,a,"object"==typeof window&&window,"object"==typeof self&&self,"object"==typeof global&&global];for(var b=0;b<a.length;++b){var c=a[b];if(c&&c.Math==Math)return c}throw Error("a");};Fb=Eb(this);Gb=function(a,b){if(b)a:{var c=Fb;a=a.split(".");for(var d=0;d<a.length-1;d++){var e=a[d];if(!(e in c))break a;c=c[e]}a=a[a.length-1];d=c[a];b=b(d);b!=d&&b!=null&&Db(c,a,{configurable:!0,writable:!0,value:b})}};Gb("globalThis",function(a){return a||Fb});
Gb("Symbol.dispose",function(a){return a?a:Symbol("b")});Gb("Promise.prototype.finally",function(a){return a?a:function(b){return this.then(function(c){return Promise.resolve(b()).then(function(){return c})},function(c){return Promise.resolve(b()).then(function(){throw c;})})}});
Gb("Array.prototype.flat",function(a){return a?a:function(b){b=b===void 0?1:b;var c=[];Array.prototype.forEach.call(this,function(d){Array.isArray(d)&&b>0?(d=Array.prototype.flat.call(d,b-1),c.push.apply(c,d)):c.push(d)});return c}});var Jb,Kb,Nb;_.Hb=_.Hb||{};_.t=this||self;Jb=function(a,b){var c=_.Ib("WIZ_global_data.oxN3nb");a=c&&c[a];return a!=null?a:b};Kb=_.t._F_toggles_gbar_||[];_.Ib=function(a,b){a=a.split(".");b=b||_.t;for(var c=0;c<a.length;c++)if(b=b[a[c]],b==null)return null;return b};_.Ka=function(a){var b=typeof a;return b!="object"?b:a?Array.isArray(a)?"array":b:"null"};_.Lb=function(a){var b=typeof a;return b=="object"&&a!=null||b=="function"};_.Mb="closure_uid_"+(Math.random()*1E9>>>0);
Nb=function(a,b,c){return a.call.apply(a.bind,arguments)};_.z=function(a,b,c){_.z=Nb;return _.z.apply(null,arguments)};_.Ob=function(a,b){var c=Array.prototype.slice.call(arguments,1);return function(){var d=c.slice();d.push.apply(d,arguments);return a.apply(this,d)}};_.A=function(a,b){a=a.split(".");for(var c=_.t,d;a.length&&(d=a.shift());)a.length||b===void 0?c[d]&&c[d]!==Object.prototype[d]?c=c[d]:c=c[d]={}:c[d]=b};_.Wa=function(a){return a};
_.B=function(a,b){function c(){}c.prototype=b.prototype;a.X=b.prototype;a.prototype=new c;a.prototype.constructor=a;a.nk=function(d,e,f){for(var g=Array(arguments.length-2),h=2;h<arguments.length;h++)g[h-2]=arguments[h];return b.prototype[e].apply(d,g)}};_.B(_.aa,Error);_.aa.prototype.name="CustomError";var Pb=!!(Kb[0]>>15&1),Qb=!!(Kb[0]&1024),Rb=!!(Kb[0]>>16&1),Sb=!!(Kb[0]&128);var Tb=Jb(1,!0),na=Pb?Rb:Jb(610401301,!1),kb=Pb?Qb||!Sb:Jb(748402147,Tb);_.Ub=_.ba(a=>a!==null&&a!==void 0);var ea=_.ba(a=>typeof a==="number"),da=_.ba(a=>typeof a==="string"),ha=_.ba(a=>typeof a==="boolean");var fa=typeof _.t.BigInt==="function"&&typeof _.t.BigInt(0)==="bigint";var Xb,Vb,Yb,Wb;_.db=_.ba(a=>fa?a>=Vb&&a<=Wb:a[0]==="-"?ja(a,Xb):ja(a,Yb));Xb=Number.MIN_SAFE_INTEGER.toString();Vb=fa?BigInt(Number.MIN_SAFE_INTEGER):void 0;Yb=Number.MAX_SAFE_INTEGER.toString();Wb=fa?BigInt(Number.MAX_SAFE_INTEGER):void 0;_.Zb=typeof TextDecoder!=="undefined";_.$b=typeof TextEncoder!=="undefined";var oa,ac=_.t.navigator;oa=ac?ac.userAgentData||null:null;_.Aa=function(a,b){return Array.prototype.indexOf.call(a,b,void 0)};_.bc=function(a,b,c){Array.prototype.forEach.call(a,b,c)};_.cc=function(a,b){return Array.prototype.some.call(a,b,void 0)};_.dc=function(a){_.dc[" "](a);return a};_.dc[" "]=function(){};var rc;_.ec=_.ra();_.fc=_.sa();_.hc=_.u("Edge");_.ic=_.u("Gecko")&&!(_.ma()&&!_.u("Edge"))&&!(_.u("Trident")||_.u("MSIE"))&&!_.u("Edge");_.jc=_.ma()&&!_.u("Edge");_.kc=_.za();_.lc=wa()?oa.platform==="Windows":_.u("Windows");_.mc=wa()?oa.platform==="Android":_.u("Android");_.nc=xa();_.oc=_.u("iPad");_.pc=_.u("iPod");_.qc=_.ya();
a:{let a="";const b=function(){const c=_.la();if(_.ic)return/rv:([^\);]+)(\)|;)/.exec(c);if(_.hc)return/Edge\/([\d\.]+)/.exec(c);if(_.fc)return/\b(?:MSIE|rv)[: ]([^\);]+)(\)|;)/.exec(c);if(_.jc)return/WebKit\/(\S+)/.exec(c);if(_.ec)return/(?:Version)[ \/]?(\S+)/.exec(c)}();b&&(a=b?b[1]:"");if(_.fc){var sc;const c=_.t.document;sc=c?c.documentMode:void 0;if(sc!=null&&sc>parseFloat(a)){rc=String(sc);break a}}rc=a}_.tc=rc;_.uc=_.ta();_.vc=xa()||_.u("iPod");_.wc=_.u("iPad");_.xc=_.u("Android")&&!(ua()||_.ta()||_.ra()||_.u("Silk"));_.yc=ua();_.zc=_.va()&&!_.ya();var Za,nb,hb;_.Xa=_.Ca();_.Ac=_.Ca();Za=_.Ca();_.Bc=_.Ca();nb=_.Ca();_.Ta=_.Ca("m_m",!0);hb=_.Ca();_.Cc=_.Ca();var Ec;_.v=_.Ca("jas",!0);Ec=[];Ec[_.v]=7;_.Dc=Object.freeze(Ec);var Da;_.Ua={};Da={};_.Fc=Object.freeze({});var ib={};var Ia=void 0;_.Gc=typeof BigInt==="function"?BigInt.asIntN:void 0;_.Hc=Number.isSafeInteger;_.Na=Number.isFinite;_.Ic=Math.trunc;var ab;_.Jc=_.ia(0);_.Kc={};_.Lc=function(a,b,c,d,e){b=_.yb(a.fa,b,c,e);if(b!==null||d&&a.o!==Da)return b};_.yb=function(a,b,c,d){if(b===-1)return null;const e=b+(c?0:-1),f=a.length-1;let g,h;if(!(f<1+(c?0:-1))){if(e>=f)if(g=a[f],g!=null&&typeof g==="object"&&g.constructor===Object)c=g[b],h=!0;else if(e===f)c=g;else return;else c=a[e];if(d&&c!=null){d=d(c);if(d==null)return d;if(!Object.is(d,c))return h?g[b]=d:a[e]=d,d}return c}};_.Mc=function(a,b,c,d){_.vb(a);const e=a.fa;_.xb(e,e[_.v]|0,b,c,d);return a};
_.C=function(a,b,c,d){let e=a.fa,f=e[_.v]|0;b=_.zb(e,f,b,c,d);if(b==null)return b;f=e[_.v]|0;if(!_.Ea(a,f)){const g=_.tb(b);g!==b&&(_.ub(a)&&(e=a.fa,f=e[_.v]|0),b=g,f=_.xb(e,f,c,b,d),_.wb(e,f))}return b};_.E=function(a,b,c){c==null&&(c=void 0);_.Mc(a,b,c);c&&!_.Ea(c)&&_.wb(a.fa);return a};_.Nc=function(a,b,c,d){return _.Pa(_.Lc(a,b,c,d))};_.F=function(a,b,c=!1,d){let e;return(e=_.Ma(_.Lc(a,b,d)))!=null?e:c};_.G=function(a,b,c="",d){let e;return(e=_.Sa(_.Lc(a,b,d)))!=null?e:c};
_.I=function(a,b,c){return _.Sa(_.Lc(a,b,c,_.Kc))};_.J=function(a,b,c,d){return _.Mc(a,b,c==null?c:_.La(c),d)};_.K=function(a,b,c){return _.Mc(a,b,c==null?c:_.Qa(c))};_.L=function(a,b,c,d){return _.Mc(a,b,_.Ra(c),d)};_.N=function(a,b,c,d){return _.Mc(a,b,c==null?c:_.Oa(c),d)};_.O=class{constructor(a,b,c){this.fa=_.mb(a,b,c)}toJSON(){return jb(this)}wa(a){return JSON.stringify(jb(this,a))}};_.O.prototype[_.Ta]=_.Ua;_.O.prototype.toString=function(){return this.fa.toString()};_.Oc=_.Ab();_.Pc=_.Ab();_.Rc=_.Ab();_.Sc=Symbol();var Tc=class extends _.O{constructor(a){super(a)}};_.Uc=class extends _.O{constructor(a){super(a)}D(a){return _.K(this,3,a)}};var Vc=class extends _.O{constructor(a){super(a)}Wb(a){return _.L(this,24,a)}};_.Wc=class extends _.O{constructor(a){super(a)}};_.P=function(){this.qa=this.qa;this.Y=this.Y};_.P.prototype.qa=!1;_.P.prototype.isDisposed=function(){return this.qa};_.P.prototype.dispose=function(){this.qa||(this.qa=!0,this.R())};_.P.prototype[Symbol.dispose]=function(){this.dispose()};_.P.prototype.R=function(){if(this.Y)for(;this.Y.length;)this.Y.shift()()};var Xc=class extends _.P{constructor(){var a=window;super();this.o=a;this.i=[];this.j={}}resolve(a){let b=this.o;a=a.split(".");const c=a.length;for(let d=0;d<c;++d)if(b[a[d]])b=b[a[d]];else return null;return b instanceof Function?b:null}tb(){const a=this.i.length,b=this.i,c=[];for(let d=0;d<a;++d){const e=b[d].i(),f=this.resolve(e);if(f&&f!=this.j[e])try{b[d].tb(f)}catch(g){}else c.push(b[d])}this.i=c.concat(b.slice(a))}};var Zc=class extends _.P{constructor(){var a=_.Yc;super();this.o=a;this.A=this.i=null;this.v=0;this.B={};this.j=!1;a=window.navigator.userAgent;a.indexOf("MSIE")>=0&&a.indexOf("Trident")>=0&&(a=/\b(?:MSIE|rv)[: ]([^\);]+)(\)|;)/.exec(a))&&a[1]&&parseFloat(a[1])<9&&(this.j=!0)}C(a,b){this.i=b;this.A=a;b.preventDefault?b.preventDefault():b.returnValue=!1}};_.$c=class extends _.O{constructor(a){super(a)}};var ad=class extends _.O{constructor(a){super(a)}};var dd;_.bd=function(a,b,c=98,d=new _.Uc){if(a.i){const e=new Tc;_.L(e,1,b.message);_.L(e,2,b.stack);_.K(e,3,b.lineNumber);_.N(e,5,1);_.E(d,40,e);a.i.log(c,d)}};dd=class{constructor(){var a=cd;this.i=null;_.F(a,4,!0)}log(a,b,c=new _.Uc){_.bd(this,a,98,c)}};var ed,fd;ed=function(a){if(a.o.length>0){var b=a.i!==void 0,c=a.j!==void 0;if(b||c){b=b?a.v:a.A;c=a.o;a.o=[];try{_.bc(c,b,a)}catch(d){console.error(d)}}}};_.gd=class{constructor(a){this.i=a;this.j=void 0;this.o=[]}then(a,b,c){this.o.push(new fd(a,b,c));ed(this)}resolve(a){if(this.i!==void 0||this.j!==void 0)throw Error("v");this.i=a;ed(this)}reject(a){if(this.i!==void 0||this.j!==void 0)throw Error("v");this.j=a;ed(this)}v(a){a.j&&a.j.call(a.i,this.i)}A(a){a.o&&a.o.call(a.i,this.j)}};
fd=class{constructor(a,b,c){this.j=a;this.o=b;this.i=c}};_.hd=a=>{var b="qc";if(a.qc&&a.hasOwnProperty(b))return a.qc;b=new a;return a.qc=b};_.R=class{constructor(){this.v=new _.gd;this.i=new _.gd;this.D=new _.gd;this.B=new _.gd;this.C=new _.gd;this.A=new _.gd;this.o=new _.gd;this.j=new _.gd;this.F=new _.gd;this.G=new _.gd}K(){return this.v}qa(){return this.i}O(){return this.D}M(){return this.B}P(){return this.C}L(){return this.A}Y(){return this.o}J(){return this.j}N(){return this.F}static i(){return _.hd(_.R)}};var ld;_.jd=function(){return _.C(_.id,Vc,1)};_.kd=function(){return _.C(_.id,_.Wc,5)};ld=class extends _.O{constructor(a){super(a)}};var md;window.gbar_&&window.gbar_.CONFIG?md=window.gbar_.CONFIG[0]||{}:md=[];_.id=new ld(md);var cd=_.C(_.id,ad,3)||new ad;_.jd()||new Vc;_.Yc=new dd;_.A("gbar_._DumpException",function(a){_.Yc?_.Yc.log(a):console.error(a)});_.nd=new Zc;var pd;_.qd=function(a,b){var c=_.od.i();if(a in c.i){if(c.i[a]!=b)throw new pd;}else{c.i[a]=b;const h=c.j[a];if(h)for(let k=0,l=h.length;k<l;k++){b=h[k];var d=c.i;delete b.i[a];if(_.Cb(b.i)){for(var e=b.j.length,f=Array(e),g=0;g<e;g++)f[g]=d[b.j[g]];b.o.apply(b.v,f)}}delete c.j[a]}};_.od=class{constructor(){this.i={};this.j={}}static i(){return _.hd(_.od)}};_.rd=class extends _.aa{constructor(){super()}};pd=class extends _.rd{};_.A("gbar.A",_.gd);_.gd.prototype.aa=_.gd.prototype.then;_.A("gbar.B",_.R);_.R.prototype.ba=_.R.prototype.qa;_.R.prototype.bb=_.R.prototype.O;_.R.prototype.bd=_.R.prototype.P;_.R.prototype.bf=_.R.prototype.K;_.R.prototype.bg=_.R.prototype.M;_.R.prototype.bh=_.R.prototype.L;_.R.prototype.bj=_.R.prototype.Y;_.R.prototype.bk=_.R.prototype.J;_.R.prototype.bl=_.R.prototype.N;_.A("gbar.a",_.R.i());window.gbar&&window.gbar.ap&&window.gbar.ap(window.gbar.a);var sd=new Xc;_.qd("api",sd);
var td=_.kd()||new _.Wc,ud=window,vd=_.y(_.I(td,8));ud.__PVT=vd;_.qd("eq",_.nd);
}catch(e){_._DumpException(e)}
try{
_.wd=class extends _.O{constructor(a){super(a)}};
}catch(e){_._DumpException(e)}
try{
var xd=class extends _.O{constructor(a){super(a)}};var yd=class extends _.P{constructor(){super();this.j=[];this.i=[]}o(a,b){this.j.push({features:a,options:b!=null?b:null})}init(a,b,c){window.gapi={};const d=window.___jsl={};d.h=_.y(_.I(a,1));_.Ma(_.Lc(a,12))!=null&&(d.dpo=_.x(_.F(a,12)));d.ms=_.y(_.I(a,2));d.m=_.y(_.I(a,3));d.l=[];_.G(b,1)&&(a=_.I(b,3))&&this.i.push(a);_.G(c,1)&&(c=_.I(c,2))&&this.i.push(c);_.A("gapi.load",(0,_.z)(this.o,this));return this}};var zd=_.C(_.id,_.$c,14);if(zd){var Bd=_.C(_.id,_.wd,9)||new _.wd,Cd=new xd,Dd=new yd;Dd.init(zd,Bd,Cd);_.qd("gs",Dd)};
}catch(e){_._DumpException(e)}
})(this.gbar_);
// Google Inc.
</script><script id="ogb-head-script2">this.gbar_=this.gbar_||{};(function(_){var window=this;
try{
_.Ed=function(a,b,c){if(!a.j)if(c instanceof Array)for(var d of c)_.Ed(a,b,d);else{d=(0,_.z)(a.C,a,b);const e=a.v+c;a.v++;b.dataset.eqid=e;a.B[e]=d;b&&b.addEventListener?b.addEventListener(c,d,!1):b&&b.attachEvent?b.attachEvent("on"+c,d):a.o.log(Error("t`"+b))}};
}catch(e){_._DumpException(e)}
try{
var Fd=document.querySelector(".gb_J .gb_B"),Gd=document.querySelector("#gb.gb_Tc");Fd&&!Gd&&_.Ed(_.nd,Fd,"click");
}catch(e){_._DumpException(e)}
try{
_.mh=function(a){if(a.v)return a.v;for(const b in a.i)if(a.i[b].ha()&&a.i[b].B())return a.i[b];return null};_.nh=function(a,b){a.i[b.J()]=b};var oh=new class extends _.P{constructor(){var a=_.Yc;super();this.B=a;this.v=null;this.o={};this.C={};this.i={};this.j=null}A(a){this.i[a]&&(_.mh(this)&&_.mh(this).J()==a||this.i[a].P(!0))}Ra(a){this.j=a;for(const b in this.i)this.i[b].ha()&&this.i[b].Ra(a)}kc(a){return a in this.i?this.i[a]:null}};_.qd("dd",oh);
}catch(e){_._DumpException(e)}
try{
_.Fi=function(a,b){return _.J(a,36,b)};
}catch(e){_._DumpException(e)}
try{
var Gi=document.querySelector(".gb_z .gb_B"),Hi=document.querySelector("#gb.gb_Tc");Gi&&!Hi&&_.Ed(_.nd,Gi,"click");
}catch(e){_._DumpException(e)}
})(this.gbar_);
// Google Inc.
</script><script id="ogb-head-script3">this.gbar_=this.gbar_||{};(function(_){var window=this;
try{
var Id;Id=class extends _.rd{};_.Jd=function(a,b){if(b in a.i)return a.i[b];throw new Id;};_.Kd=function(a){return _.Jd(_.od.i(),a)};
}catch(e){_._DumpException(e)}
try{
/*

 Copyright Google LLC
 SPDX-License-Identifier: Apache-2.0
*/
var Nd;_.Ld=function(a){const b=a.length;if(b>0){const c=Array(b);for(let d=0;d<b;d++)c[d]=a[d];return c}return[]};Nd=function(a){return new _.Md(b=>b.substr(0,a.length+1).toLowerCase()===a+":")};_.Od=globalThis.trustedTypes;_.Pd=class{constructor(a){this.i=a}toString(){return this.i}};_.Qd=new _.Pd("about:invalid#zClosurez");_.Md=class{constructor(a){this.Th=a}};_.Rd=[Nd("data"),Nd("http"),Nd("https"),Nd("mailto"),Nd("ftp"),new _.Md(a=>/^[^:]*([/?#]|$)/.test(a))];_.Sd=class{constructor(a){this.i=a}toString(){return this.i+""}};_.Td=new _.Sd(_.Od?_.Od.emptyHTML:"");
}catch(e){_._DumpException(e)}
try{
var Xd,ie,Wd,Yd,ce;_.Ud=function(a){if(a==null)return a;if(typeof a==="string"&&a)a=+a;else if(typeof a!=="number")return;return(0,_.Na)(a)?a|0:void 0};_.Vd=function(a,b){return a.lastIndexOf(b,0)==0};Xd=function(){let a=null;if(!Wd)return a;try{const b=c=>c;a=Wd.createPolicy("ogb-qtm#html",{createHTML:b,createScript:b,createScriptURL:b})}catch(b){}return a};_.Zd=function(){Yd===void 0&&(Yd=Xd());return Yd};_.ae=function(a){const b=_.Zd();a=b?b.createScriptURL(a):a;return new _.$d(a)};
_.be=function(a){if(a instanceof _.$d)return a.i;throw Error("x");};_.de=function(a){if(ce.test(a))return a};_.ee=function(a){if(a instanceof _.Pd)if(a instanceof _.Pd)a=a.i;else throw Error("x");else a=_.de(a);return a};_.fe=function(a,b=document){let c;const d=(c=b.querySelector)==null?void 0:c.call(b,`${a}[nonce]`);return d==null?"":d.nonce||d.getAttribute("nonce")||""};_.S=function(a,b,c){return _.Ma(_.Lc(a,b,c,_.Kc))};_.ge=function(a,b){return _.Ud(_.Lc(a,b,void 0,_.Kc))};
_.he=function(a){var b=_.Ka(a);return b=="array"||b=="object"&&typeof a.length=="number"};Wd=_.Od;_.$d=class{constructor(a){this.i=a}toString(){return this.i+""}};ce=/^\s*(?!javascript:)(?:[\w+.-]+:|[^:/?#]*(?:[/?#]|$))/i;var oe,se,je;_.le=function(a){return a?new je(_.ke(a)):ie||(ie=new je)};_.me=function(a,b){return typeof b==="string"?a.getElementById(b):b};_.T=function(a,b){var c=b||document;c.getElementsByClassName?a=c.getElementsByClassName(a)[0]:(c=document,a=a?(b||c).querySelector(a?"."+a:""):_.ne(c,"*",a,b)[0]||null);return a||null};_.ne=function(a,b,c,d){a=d||a;return(b=b&&b!="*"?String(b).toUpperCase():"")||c?a.querySelectorAll(b+(c?"."+c:"")):a.getElementsByTagName("*")};
_.pe=function(a,b){_.Bb(b,function(c,d){d=="style"?a.style.cssText=c:d=="class"?a.className=c:d=="for"?a.htmlFor=c:oe.hasOwnProperty(d)?a.setAttribute(oe[d],c):_.Vd(d,"aria-")||_.Vd(d,"data-")?a.setAttribute(d,c):a[d]=c})};oe={cellpadding:"cellPadding",cellspacing:"cellSpacing",colspan:"colSpan",frameborder:"frameBorder",height:"height",maxlength:"maxLength",nonce:"nonce",role:"role",rowspan:"rowSpan",type:"type",usemap:"useMap",valign:"vAlign",width:"width"};
_.qe=function(a){return a?a.defaultView:window};_.te=function(a,b){const c=b[1],d=_.re(a,String(b[0]));c&&(typeof c==="string"?d.className=c:Array.isArray(c)?d.className=c.join(" "):_.pe(d,c));b.length>2&&se(a,d,b);return d};se=function(a,b,c){function d(e){e&&b.appendChild(typeof e==="string"?a.createTextNode(e):e)}for(let e=2;e<c.length;e++){const f=c[e];!_.he(f)||_.Lb(f)&&f.nodeType>0?d(f):_.bc(f&&typeof f.length=="number"&&typeof f.item=="function"?_.Ld(f):f,d)}};
_.ue=function(a){return _.re(document,a)};_.re=function(a,b){b=String(b);a.contentType==="application/xhtml+xml"&&(b=b.toLowerCase());return a.createElement(b)};_.ve=function(a){let b;for(;b=a.firstChild;)a.removeChild(b)};_.we=function(a){return a&&a.parentNode?a.parentNode.removeChild(a):null};_.xe=function(a,b){return a&&b?a==b||a.contains(b):!1};_.ke=function(a){return a.nodeType==9?a:a.ownerDocument||a.document};je=function(a){this.i=a||_.t.document||document};_.n=je.prototype;
_.n.H=function(a){return _.me(this.i,a)};_.n.Pa=function(a,b,c){return _.te(this.i,arguments)};_.n.appendChild=function(a,b){a.appendChild(b)};_.n.Je=_.ve;_.n.ng=_.we;_.n.mg=_.xe;
}catch(e){_._DumpException(e)}
try{
_.Mi=function(a){const b=_.fe("script",a.ownerDocument);b&&a.setAttribute("nonce",b)};_.Ni=function(a){if(!a)return null;a=_.I(a,4);var b;a===null||a===void 0?b=null:b=_.ae(a);return b};_.Oi=function(a,b,c){a=a.fa;return _.zb(a,a[_.v]|0,b,c)!==void 0};_.Pi=class extends _.O{constructor(a){super(a)}};_.Qi=function(a,b){return(b||document).getElementsByTagName(String(a))};
}catch(e){_._DumpException(e)}
try{
var Si=function(a,b,c){a<b?Ri(a+1,b):_.Yc.log(Error("W`"+a+"`"+b),{url:c})},Ri=function(a,b){if(Ti){const c=_.ue("SCRIPT");c.async=!0;c.type="text/javascript";c.charset="UTF-8";c.src=_.be(Ti);_.Mi(c);c.onerror=_.Ob(Si,a,b,c.src);_.Qi("HEAD")[0].appendChild(c)}},Ui=class extends _.O{constructor(a){super(a)}};var Vi=_.C(_.id,Ui,17)||new Ui,Wi,Ti=(Wi=_.C(Vi,_.Pi,1))?_.Ni(Wi):null,Xi,Yi=(Xi=_.C(Vi,_.Pi,2))?_.Ni(Xi):null,Zi=function(){Ri(1,2);if(Yi){const a=_.ue("LINK");a.setAttribute("type","text/css");a.href=_.be(Yi).toString();a.rel="stylesheet";let b=_.fe("style",document);b&&a.setAttribute("nonce",b);_.Qi("HEAD")[0].appendChild(a)}};(function(){const a=_.jd();if(_.S(a,18))Zi();else{const b=_.ge(a,19)||0;window.addEventListener("load",()=>{window.setTimeout(Zi,b)})}})();
}catch(e){_._DumpException(e)}
})(this.gbar_);
// Google Inc.
</script><script async="" type="text/javascript" charset="UTF-8" src="https://www.gstatic.com/og/_/js/k=og.qtm.en_US.v2pk7dVghog.2019.O/rt=j/m=qabr,qgl,q_dnp,qcwid,qbd,qapid,qads,qrcd,q_dg/exm=qaaw,qadd,qaid,qein,qhaw,qhba,qhbr,qhch,qhga,qhid,qhin/d=1/ed=1/rs=AA2YrTthfa-GW6nWNiVo32au3OStcP0_zg" nonce=""></script><link type="text/css" href="https://www.gstatic.com/og/_/ss/k=og.qtm.5bOMfS7uCn8.L.W.O/m=qcwid,qba/excm=qaaw,qadd,qaid,qein,qhaw,qhba,qhbr,qhch,qhga,qhid,qhin/d=1/ed=1/ct=zgms/rs=AA2YrTs5z5IeveM3_8fj3UK_0H1gj7fqJg" rel="stylesheet"><script type="text/javascript" charset="UTF-8" src="https://apis.google.com/js/api.js" nonce="" gapi_processed="true"></script><script type="text/javascript" async="" src="https://googleads.g.doubleclick.net/pagead/viewthroughconversion/11082232239/?random=1755363734501&amp;cv=11&amp;fst=1755363734501&amp;bg=ffffff&amp;guid=ON&amp;async=1&amp;gtm=45be58d1v9101670439z89175119176za200zb9175119176zd6343254xea&amp;gcd=13r3r3l3l5l1&amp;dma=0&amp;tag_exp=101509157~103116026~103200004~103233427~104527907~104528501~104684208~104684211~104948811~104948813~105033766~105033768~105102052~105103161~105103163~105231383~105231385~105347236&amp;u_w=1536&amp;u_h=864&amp;url=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Fdocs%2Fpartitioned-tables&amp;hn=www.googleadservices.com&amp;frm=0&amp;tiba=Introduction%20to%20partitioned%20tables%20%C2%A0%7C%C2%A0%20BigQuery%20%C2%A0%7C%C2%A0%20Google%20Cloud&amp;npa=0&amp;pscdl=noapi&amp;auid=1703008205.1751311484&amp;uaa=x86&amp;uab=64&amp;uafvl=Not)A%253BBrand%3B8.0.0.0%7CChromium%3B138.0.7204.184%7CGoogle%2520Chrome%3B138.0.7204.184&amp;uamb=0&amp;uam=&amp;uap=Windows&amp;uapv=19.0.0&amp;uaw=0&amp;_tu=Cg&amp;rfmt=3&amp;fmt=4" nonce=""></script><script type="text/javascript" async="" src="https://googleads.g.doubleclick.net/pagead/viewthroughconversion/10836211492/?random=1755363734520&amp;cv=11&amp;fst=1755363734520&amp;bg=ffffff&amp;guid=ON&amp;async=1&amp;gtm=45be58d1v875695591z89175119176za200zb9175119176zd6343254xea&amp;gcd=13r3r3l3l5l1&amp;dma=0&amp;tag_exp=101509157~103116026~103200004~103233427~104527907~104528500~104684208~104684211~104948813~105033766~105033768~105103161~105103163~105231383~105231385&amp;u_w=1536&amp;u_h=864&amp;url=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Fdocs%2Fpartitioned-tables&amp;hn=www.googleadservices.com&amp;frm=0&amp;tiba=Introduction%20to%20partitioned%20tables%20%C2%A0%7C%C2%A0%20BigQuery%20%C2%A0%7C%C2%A0%20Google%20Cloud&amp;npa=0&amp;pscdl=noapi&amp;auid=1703008205.1751311484&amp;uaa=x86&amp;uab=64&amp;uafvl=Not)A%253BBrand%3B8.0.0.0%7CChromium%3B138.0.7204.184%7CGoogle%2520Chrome%3B138.0.7204.184&amp;uamb=0&amp;uam=&amp;uap=Windows&amp;uapv=19.0.0&amp;uaw=0&amp;_tu=Cg&amp;rfmt=3&amp;fmt=4" nonce=""></script><script type="text/javascript" async="" src="https://googleads.g.doubleclick.net/pagead/viewthroughconversion/16541431319/?random=1755363734535&amp;cv=11&amp;fst=1755363734535&amp;bg=ffffff&amp;guid=ON&amp;async=1&amp;gtm=45be58d1v9183668572z89175119176za200zb9175119176zd6343254xea&amp;gcd=13r3r3l3l5l1&amp;dma=0&amp;tag_exp=101509157~103116026~103200004~103233427~104527907~104528501~104684208~104684211~104948813~105033766~105033768~105102052~105103161~105103163~105231383~105231385&amp;u_w=1536&amp;u_h=864&amp;url=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Fdocs%2Fpartitioned-tables&amp;hn=www.googleadservices.com&amp;frm=0&amp;tiba=Introduction%20to%20partitioned%20tables%20%C2%A0%7C%C2%A0%20BigQuery%20%C2%A0%7C%C2%A0%20Google%20Cloud&amp;npa=0&amp;pscdl=noapi&amp;auid=1703008205.1751311484&amp;uaa=x86&amp;uab=64&amp;uafvl=Not)A%253BBrand%3B8.0.0.0%7CChromium%3B138.0.7204.184%7CGoogle%2520Chrome%3B138.0.7204.184&amp;uamb=0&amp;uam=&amp;uap=Windows&amp;uapv=19.0.0&amp;uaw=0&amp;_tu=Kg&amp;rfmt=3&amp;fmt=4" nonce=""></script></head>
  <body class="tenant--cloud viewport--tablet" template="page" theme="cloud-theme" type="article" layout="docs" display-toc="" ready="" signed-in="" style="--devsite-panel-height: 0px; --devsite-js-header-height: 112.80000305175781px;">
    <devsite-progress id="app-progress"></devsite-progress>
  
    <a href="#main-content" class="skip-link button">
      
      Skip to main content
    </a>
    <section class="devsite-wrapper">
      <devsite-cookie-notification-bar><!----></devsite-cookie-notification-bar><cloudx-track usercountry="US"></cloudx-track>
<cloudx-utils-init></cloudx-utils-init>

<devsite-header keep-tabs-visible="" fixed="" top-row--height="64.80000305175781" bottom-row--height="48" bottom-tabs--height="48" style="--devsite-js-top-row--height: 64.80000305175781px; --devsite-js-bottom-row--height: 48px; --devsite-js-bottom-tabs--height: 48px;">
  
    





















<div class="devsite-header--inner" data-nosnippet="">
  <div class="devsite-top-logo-row-wrapper-wrapper">
    <div class="devsite-top-logo-row-wrapper">
      <div class="devsite-top-logo-row">
        <button type="button" id="devsite-hamburger-menu" class="devsite-header-icon-button button-flat material-icons gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Navigation menu button" aria-label="Open menu">
        </button>
        
<div class="devsite-product-name-wrapper">

  <a href="/" class="devsite-site-logo-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Site logo" track-type="globalNav" track-name="googleCloud" track-metadata-position="nav" track-metadata-eventdetail="nav">
  
  <picture>
    
    <img src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/cloud-logo.svg" class="devsite-site-logo" alt="Google Cloud">
  </picture>
  
</a>



  
  
  <span class="devsite-product-name">
    <ul class="devsite-breadcrumb-list">
  
  <li class="devsite-breadcrumb-item
             devsite-has-google-wordmark">
    
    
    
      
      
    
  </li>
  
</ul>
  </span>

</div>
        <div class="devsite-top-logo-row-middle">
          <div class="devsite-header-upper-tabs">
            
              
              
  <cloudx-tabs-nav class="upper-tabs" connected="">

    <div class="devsite-overflow-cover devsite-left-overflow"></div><button class="devsite-scroll-button devsite-scroll-left" aria-label="Scroll to previous navigation items"></button><nav class="devsite-tabs-wrapper" aria-label="Upper tabs" style="--scroll-animation-duration: 250ms; --scroll-offset: 0px;">
      
        
          <tab class="devsite-active">
            
    <a href="https://cloud.google.com/docs" class="devsite-tabs-content gc-analytics-event " track-metadata-eventdetail="https://cloud.google.com/docs" track-type="nav" track-metadata-position="nav - docs-home" track-metadata-module="primary nav" aria-label="Documentation, selected" data-category="Site-Wide Custom Events" data-label="Tab: Documentation" track-name="docs-home" track-link-column-type="single-column">
    Documentation
  
    </a>
    
  
          </tab>
        
      
        
          <tab class="devsite-dropdown
    
    
    devsite-clickable
    ">
  
    <a href="https://cloud.google.com/docs/tech-area-overviews" class="devsite-tabs-content gc-analytics-event " track-metadata-eventdetail="https://cloud.google.com/docs/tech-area-overviews" track-type="nav" track-metadata-position="nav - technology-areas" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Technology areas" track-name="technology-areas" track-link-column-type="single-column">
    Technology areas
  
    </a>
    
      <button aria-haspopup="menu" aria-expanded="false" aria-label="Dropdown menu for Technology areas" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/tech-area-overviews" track-metadata-position="nav - technology-areas" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Technology areas" track-name="technology-areas" track-link-column-type="single-column" class="devsite-tabs-dropdown-toggle devsite-icon devsite-icon-arrow-drop-down"></button>
    
  
  <div class="devsite-tabs-dropdown" role="menu" aria-label="submenu" hidden="">
    
      <button class="devsite-tabs-close-button material-icons button-flat gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Close dropdown menu" aria-label="Close dropdown menu" track-type="nav" track-name="close" track-metadata-eventdetail="#" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav">close</button>
    
    <div class="devsite-tabs-dropdown-content">
      
        <div class="devsite-tabs-dropdown-column
                    ">
          
            <ul class="devsite-tabs-dropdown-section
                       ">
              
              
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/ai-ml" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/ai-ml" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      AI and ML
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/application-development" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/application-development" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Application development
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/application-hosting" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/application-hosting" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Application hosting
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/compute-area" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/compute-area" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Compute
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/data" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/data" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Data analytics and pipelines
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/databases" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/databases" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Databases
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/dhm-cloud" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/dhm-cloud" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Distributed, hybrid, and multicloud
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/generative-ai" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/generative-ai" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Generative AI
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/industry" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/industry" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Industry solutions
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/networking" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/networking" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Networking
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/observability" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/observability" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Observability and monitoring
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/security" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/security" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Security
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/storage" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/storage" track-metadata-position="nav - technology-areas" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Storage
                    </div>
                    
                  </a>
                </li>
              
            </ul>
          
        </div>
      
    </div>
  </div>
</tab>
        
      
        
          <tab class="devsite-dropdown
    
    
    devsite-clickable
    ">
  
    <a href="https://cloud.google.com/docs/cross-product-overviews" class="devsite-tabs-content gc-analytics-event " track-metadata-eventdetail="https://cloud.google.com/docs/cross-product-overviews" track-type="nav" track-metadata-position="nav - crossproduct" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Cross-product tools" track-name="crossproduct" track-link-column-type="single-column">
    Cross-product tools
  
    </a>
    
      <button aria-haspopup="menu" aria-expanded="false" aria-label="Dropdown menu for Cross-product tools" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/cross-product-overviews" track-metadata-position="nav - crossproduct" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Cross-product tools" track-name="crossproduct" track-link-column-type="single-column" class="devsite-tabs-dropdown-toggle devsite-icon devsite-icon-arrow-drop-down"></button>
    
  
  <div class="devsite-tabs-dropdown" role="menu" aria-label="submenu" hidden="">
    
      <button class="devsite-tabs-close-button material-icons button-flat gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Close dropdown menu" aria-label="Close dropdown menu" track-type="nav" track-name="close" track-metadata-eventdetail="#" track-metadata-position="nav - crossproduct" track-metadata-module="tertiary nav">close</button>
    
    <div class="devsite-tabs-dropdown-content">
      
        <div class="devsite-tabs-dropdown-column
                    ">
          
            <ul class="devsite-tabs-dropdown-section
                       ">
              
              
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/access-resources" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/access-resources" track-metadata-position="nav - crossproduct" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Access and resources management
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/costs-usage" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/costs-usage" track-metadata-position="nav - crossproduct" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Costs and usage management
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/devtools" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/devtools" track-metadata-position="nav - crossproduct" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud SDK, languages, frameworks, and tools
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/iac" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/iac" track-metadata-position="nav - crossproduct" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Infrastructure as code
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/docs/migration" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/docs/migration" track-metadata-position="nav - crossproduct" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Migration
                    </div>
                    
                  </a>
                </li>
              
            </ul>
          
        </div>
      
    </div>
  </div>
</tab>
        
      
        
          <tab class="devsite-dropdown
    
    
    devsite-clickable
    ">
  
    <a href="https://cloud.google.com/" class="devsite-tabs-content gc-analytics-event " track-metadata-eventdetail="https://cloud.google.com/" track-type="nav" track-metadata-position="nav - related-sites" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Related sites" track-name="related-sites" track-link-column-type="single-column">
    Related sites
  
    </a>
    
      <button aria-haspopup="menu" aria-expanded="false" aria-label="Dropdown menu for Related sites" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/" track-metadata-position="nav - related-sites" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Related sites" track-name="related-sites" track-link-column-type="single-column" class="devsite-tabs-dropdown-toggle devsite-icon devsite-icon-arrow-drop-down"></button>
    
  
  <div class="devsite-tabs-dropdown" role="menu" aria-label="submenu" hidden="">
    
      <button class="devsite-tabs-close-button material-icons button-flat gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Close dropdown menu" aria-label="Close dropdown menu" track-type="nav" track-name="close" track-metadata-eventdetail="#" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav">close</button>
    
    <div class="devsite-tabs-dropdown-content">
      
        <div class="devsite-tabs-dropdown-column
                    ">
          
            <ul class="devsite-tabs-dropdown-section
                       ">
              
              
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud Home
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/free" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/free" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Free Trial and Free Tier
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/architecture" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/architecture" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Architecture Center
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/blog" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/blog" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Blog
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/contact" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/contact" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Contact Sales
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/developers" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/developers" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud Developer Center
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://developers.google.com/" track-type="nav" track-metadata-eventdetail="https://developers.google.com/" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Developer Center
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://console.cloud.google.com/marketplace" track-type="nav" track-metadata-eventdetail="https://console.cloud.google.com/marketplace" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud Marketplace
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/marketplace/docs" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/marketplace/docs" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud Marketplace Documentation
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://www.cloudskillsboost.google/paths" track-type="nav" track-metadata-eventdetail="https://www.cloudskillsboost.google/paths" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud Skills Boost
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/solutions" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/solutions" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud Solution Center
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://cloud.google.com/support-hub" track-type="nav" track-metadata-eventdetail="https://cloud.google.com/support-hub" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud Support
                    </div>
                    
                  </a>
                </li>
              
                <li class="devsite-nav-item">
                  <a href="https://www.youtube.com/@googlecloudtech" track-type="nav" track-metadata-eventdetail="https://www.youtube.com/@googlecloudtech" track-metadata-position="nav - related-sites" track-metadata-module="tertiary nav" tooltip="">
                    
                    <div class="devsite-nav-item-title">
                      Google Cloud Tech Youtube Channel
                    </div>
                    
                  </a>
                </li>
              
            </ul>
          
        </div>
      
    </div>
  </div>
</tab>
        
      
    <tab class="devsite-overflow-tab" style=""><!---->
          <button class="devsite-tabs-overflow-button devsite-icon devsite-icon-arrow-drop-down" aria-haspopup="menu" aria-expanded="false" id="tab-overflow-button-43th" aria-label="Dropdown menu for Extended Navigation" aria-controls="tab-overflow-menu-zmBH"><!--?lit$118760000$-->More</button>
          <div class="devsite-tabs-overflow-menu" hidden="" scrollbars="" role="menu" id="tab-overflow-menu-zmBH" aria-labelledby="tab-overflow-button-43th">
          </div>
        </tab></nav>

  <!----><button class="devsite-scroll-button devsite-scroll-right devsite-visible" aria-label="Scroll to more navigation items"></button><div class="devsite-overflow-cover devsite-right-overflow"></div></cloudx-tabs-nav>

            
           </div>
          
<devsite-search enable-signin="" enable-search="" enable-suggestions="" enable-search-summaries="" project-name="BigQuery" tenant-name="Google Cloud" project-scope="/bigquery/docs" url-scoped="https://cloud.google.com/s/results/bigquery/docs">
  <form class="devsite-search-form" action="https://cloud.google.com/s/results" method="GET">
    <div class="devsite-search-container">
      <button type="button" search-open="" class="devsite-search-button devsite-header-icon-button button-flat material-icons" aria-label="Open search"></button>
      <div class="devsite-searchbox">
        <input aria-activedescendant="" aria-autocomplete="list" aria-label="Search" aria-expanded="false" aria-haspopup="listbox" autocomplete="off" class="devsite-search-field devsite-search-query" name="q" placeholder="Search" role="combobox" type="text" value="" aria-controls="devsite-search-popout-container-id-1">
          <div class="devsite-search-image material-icons" aria-hidden="true">
            
              <svg class="devsite-search-ai-image" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <g clip-path="url(#clip0_6641_386)">
                    <path d="M19.6 21L13.3 14.7C12.8 15.1 12.225 15.4167 11.575 15.65C10.925 15.8833 10.2333 16 9.5 16C7.68333 16 6.14167 15.375 4.875 14.125C3.625 12.8583 3 11.3167 3 9.5C3 7.68333 3.625 6.15 4.875 4.9C6.14167 3.63333 7.68333 3 9.5 3C10.0167 3 10.5167 3.05833 11 3.175C11.4833 3.275 11.9417 3.43333 12.375 3.65L10.825 5.2C10.6083 5.13333 10.3917 5.08333 10.175 5.05C9.95833 5.01667 9.73333 5 9.5 5C8.25 5 7.18333 5.44167 6.3 6.325C5.43333 7.19167 5 8.25 5 9.5C5 10.75 5.43333 11.8167 6.3 12.7C7.18333 13.5667 8.25 14 9.5 14C10.6667 14 11.6667 13.625 12.5 12.875C13.35 12.1083 13.8417 11.15 13.975 10H15.975C15.925 10.6333 15.7833 11.2333 15.55 11.8C15.3333 12.3667 15.05 12.8667 14.7 13.3L21 19.6L19.6 21ZM17.5 12C17.5 10.4667 16.9667 9.16667 15.9 8.1C14.8333 7.03333 13.5333 6.5 12 6.5C13.5333 6.5 14.8333 5.96667 15.9 4.9C16.9667 3.83333 17.5 2.53333 17.5 0.999999C17.5 2.53333 18.0333 3.83333 19.1 4.9C20.1667 5.96667 21.4667 6.5 23 6.5C21.4667 6.5 20.1667 7.03333 19.1 8.1C18.0333 9.16667 17.5 10.4667 17.5 12Z" fill="#5F6368"></path>
                  </g>
                <defs>
                <clipPath id="clip0_6641_386">
                <rect width="24" height="24" fill="white"></rect>
                </clipPath>
                </defs>
              </svg>
            
          </div>
          <div class="devsite-search-shortcut-icon-container" aria-hidden="true">
            <kbd class="devsite-search-shortcut-icon">/</kbd>
          </div>
      </div>
    </div>
  <div class="devsite-popout" id="devsite-search-popout-container-id-1"><div class="devsite-popout-result devsite-suggest-results-container" devsite-hide=""></div></div></form>
  <button type="button" search-close="" class="devsite-search-button devsite-header-icon-button button-flat material-icons" aria-label="Close search"></button>
</devsite-search>

        <div class="devsite-search-background" style="opacity: 1;"></div></div>

        

  
    <devsite-shell-activate-button><button class="gc-analytics-event activate-cloudshell-button" data-category="Site-Wide Custom Events" data-label="Activate Cloud Shell" aria-label="Activate Cloud Shell" data-tooltip="Activate Cloud Shell" track-type="cloudShell" track-name="activateCloudShell"><svg width="22" height="18" viewBox="0 0 22 18" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M20 0H2C0.9 0 0 0.9 0 2V16C0 17.1 0.9 18 2 18H20C21.1 18 22 17.1 22 16V2C22 0.9 21.1 0 20 0ZM20 16.01H2V1.99H20V16.01Z"></path><path d="M6.87574 6H4.72426C4.45699 6 4.32314 6.32314 4.51213 6.51213L7.78787 9.78787C7.90503 9.90503 7.90503 10.095 7.78787 10.2121L4.51213 13.4879C4.32314 13.6769 4.45699 14 4.72426 14H6.87574C6.9553 14 7.03161 13.9684 7.08787 13.9121L10.7879 10.2121C10.905 10.095 10.905 9.90503 10.7879 9.78787L7.08787 6.08787C7.03161 6.03161 6.9553 6 6.87574 6Z"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M4.51213 6.51213C4.32314 6.32314 4.45699 6 4.72426 6H6.87574C6.9553 6 7.03161 6.03161 7.08787 6.08787L10.7879 9.78787C10.905 9.90503 10.905 10.095 10.7879 10.2121L7.08787 13.9121C7.03161 13.9684 6.9553 14 6.87574 14H4.72426C4.45699 14 4.32314 13.6769 4.51213 13.4879L7.78787 10.2121C7.90503 10.095 7.90503 9.90503 7.78787 9.78787L4.51213 6.51213ZM6.41421 7L8.49497 9.08076C9.00266 9.58844 9.00266 10.4116 8.49497 10.9192L6.41421 13H6.58579L9.58579 10L6.58579 7H6.41421Z"></path><path d="M11 13.7V12.3C11 12.1343 11.1343 12 11.3 12H17.7C17.8657 12 18 12.1343 18 12.3V13.7C18 13.8657 17.8657 14 17.7 14H11.3C11.1343 14 11 13.8657 11 13.7Z"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M11 12.3V13.7C11 13.8657 11.1343 14 11.3 14H17.7C17.8657 14 18 13.8657 18 13.7V12.3C18 12.1343 17.8657 12 17.7 12H11.3C11.1343 12 11 12.1343 11 12.3Z"></path></svg></button></devsite-shell-activate-button>
  

  

  

  

  
<devsite-language-selector aria-label="Select your language preference.">
  <ul role="presentation">
    
    
    <li role="presentation">
      <a role="menuitem" lang="en" aria-current="true" href="https://cloud.google.com/bigquery/docs/partitioned-tables">English</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="de" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=de">Deutsch</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="es-419" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=es-419">Español – América Latina</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="fr" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=fr">Français</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="pt-br" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=pt-br">Português – Brasil</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="zh-cn" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-cn">中文 – 简体</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="ja" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=ja">日本語</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="ko" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=ko">한국어</a>
    </li>
    
  </ul>
</devsite-language-selector>


  
    <a class="devsite-header-link devsite-top-button button gc-analytics-event " href="//console.cloud.google.com/" data-category="Site-Wide Custom Events" data-label="Site header link: Console" track-type="globalNav" track-metadata-position="nav" referrerpolicy="no-referrer-when-downgrade" track-name="console" track-metadata-eventdetail="nav">
  Console
</a>
  



        
          <devsite-user signed-in="" enable-profiles="" fp-auth="" id="devsite-user" sign-in-url="https://cloud.google.com/_d/signin?continue=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Fdocs%2Fpartitioned-tables&amp;prompt=select_account" sign-out-url="https://cloud.google.com/_d/signout?continue=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Fdocs%2Fpartitioned-tables" url="https://cloud.google.com/_d/signin?continue=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Fdocs%2Fpartitioned-tables&amp;prompt=select_account"><div class="ogb-wrapper ogb-so"><div class="devsite-devprofile-wrapper show"><devsite-feature-tooltip ack-key="AckViewSavedPagesPopoutDismiss" id="devsite-view-saved-pages" close-button-href="https://developers.google.com/profile/u/101193512566334334202/saved-pages" close-button-text="View" dismiss-button="" managed="" rendered="" current-step="0" style="--devsite-popout-offset-x: 32px;"><button class="devsite-devprofile-button" aria-controls="devsite-devprofile-popout" aria-expanded="false" aria-haspopup="true" aria-label="Open Google Developer Program dropdown" data-tooltip="Google Developer Program"><svg width="4" height="16" viewBox="0 0 4 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M2 4C3.1 4 4 3.1 4 2C4 0.9 3.1 0 2 0C0.9 0 0 0.9 0 2C0 3.1 0.9 4 2 4ZM2 6C0.9 6 0 6.9 0 8C0 9.1 0.9 10 2 10C3.1 10 4 9.1 4 8C4 6.9 3.1 6 2 6ZM0 14C0 12.9 0.9 12 2 12C3.1 12 4 12.9 4 14C4 15.1 3.1 16 2 16C0.9 16 0 15.1 0 14Z"></path></svg></button><span slot="popout-heading">Google Developer Program</span><span slot="popout-contents">View your saved pages and finish your Google Developer Profile setup here.</span></devsite-feature-tooltip><div id="devsite-devprofile-popout" class="devsite-devprofile-popout" role="menu" aria-label="Google Developer Program"></div><devsite-callout-notification><!----><!--?--></devsite-callout-notification></div><div class="gb_Fa gb_Kd gb_4d gb_Hd" id="gb"><div class="gb_Dd gb_1d gb_yd" ng-non-bindable="" data-ogsr-up="" style="padding:0;height:auto;display:block"><div class="gb_Te" style="display:block"><div class="gb_4c"></div><div class="gb_z gb_dd gb_Pf gb_0"><div class="gb_D gb_jb gb_Pf gb_0"><a class="gb_B gb_Za gb_0" aria-expanded="false" aria-label="Google Account: Sanket Nadkarni  
(nadkarnisanket11@gmail.com)" href="https://accounts.google.com/SignOutOptions?hl=en&amp;continue=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Fdocs%2Fpartitioned-tables&amp;ec=GBRAywI" tabindex="0" role="button"><div class="gb_3d"><svg focusable="false" height="40px" version="1.1" viewBox="0 0 40 40" width="40px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="opacity:1.0"><path d="M4.02,28.27C2.73,25.8,2,22.98,2,20c0-2.87,0.68-5.59,1.88-8l-1.72-1.04C0.78,13.67,0,16.75,0,20c0,3.31,0.8,6.43,2.23,9.18L4.02,28.27z" fill="#F6AD01"></path><path d="M32.15,33.27C28.95,36.21,24.68,38,20,38c-6.95,0-12.98-3.95-15.99-9.73l-1.79,0.91C5.55,35.61,12.26,40,20,40c5.2,0,9.93-1.98,13.48-5.23L32.15,33.27z" fill="#249A41"></path><path d="M33.49,34.77C37.49,31.12,40,25.85,40,20c0-5.86-2.52-11.13-6.54-14.79l-1.37,1.46C35.72,9.97,38,14.72,38,20c0,5.25-2.26,9.98-5.85,13.27L33.49,34.77z" fill="#3174F1"></path><path d="M20,2c4.65,0,8.89,1.77,12.09,4.67l1.37-1.46C29.91,1.97,25.19,0,20,0l0,0C12.21,0,5.46,4.46,2.16,10.96L3.88,12C6.83,6.08,12.95,2,20,2" fill="#E92D18"></path></svg></div><span class="gb_Ud"><img class="gb_P gbii" src="https://lh3.google.com/u/0/ogw/AF2bZyjkOrwzv87BjtxjPeImvYSOf1dsRjib1R8E_kkK8_jDBA=s32-c-mo" srcset="https://lh3.google.com/u/0/ogw/AF2bZyjkOrwzv87BjtxjPeImvYSOf1dsRjib1R8E_kkK8_jDBA=s32-c-mo 1x, https://lh3.google.com/u/0/ogw/AF2bZyjkOrwzv87BjtxjPeImvYSOf1dsRjib1R8E_kkK8_jDBA=s64-c-mo 2x " alt="" aria-hidden="true" data-noaft=""></span><div class="gb_Q gb_R" aria-hidden="true"><svg class="gb_Ka" height="14" viewBox="0 0 14 14" width="14" xmlns="http://www.w3.org/2000/svg"><circle class="gb_La" cx="7" cy="7" r="7"></circle><path class="gb_Na" d="M6 10H8V12H6V10ZM6 2H8V8H6V2Z"></path></svg></div></a></div></div></div><div style="overflow: hidden; position: absolute; top: 0px; visibility: hidden; width: 436px; z-index: 991; height: 0px; margin-top: 57px; right: 0px; margin-right: 4px;"></div><div style="overflow: hidden; position: absolute; top: 0px; visibility: hidden; width: 420px; z-index: 991; height: 280px; margin-top: 70px; right: 0px; margin-right: 25px;"></div></div></div></div></devsite-user>
        
        
        
      </div>
    </div>
  </div>



  <div class="devsite-collapsible-section
    " style="transform: translate3d(0px, 0px, 0px);">
    <div class="devsite-header-background">
      
        
          <div class="devsite-product-id-row" hidden="">
            <div class="devsite-product-description-row">
              
              
            </div>
            
          </div>
          
        
      
      
        <div class="devsite-doc-set-nav-row">
          
            
              <ul class="devsite-breadcrumb-list">
  
  <li class="devsite-breadcrumb-item
             ">
    
    
    
      
  <a href="https://cloud.google.com/bigquery" class="devsite-breadcrumb-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Lower Header" data-value="1" track-type="globalNav" track-name="breadcrumb" track-metadata-position="1" track-metadata-eventdetail="BigQuery: Cloud Data Warehouse">
    
        BigQuery
      
  </a>
  
    
  </li>
  
</ul>
            
          
          
            
            
  <cloudx-tabs-nav class="lower-tabs" connected="">

    <div class="devsite-overflow-cover devsite-left-overflow"></div><button class="devsite-scroll-button devsite-scroll-left" aria-label="Scroll to previous navigation items"></button><nav class="devsite-tabs-wrapper" aria-label="Lower tabs" style="--scroll-animation-duration: 250ms; --scroll-offset: 0px;">
      
        
          <tab class="devsite-active">
            
    <a href="https://cloud.google.com/bigquery/docs/introduction" class="devsite-tabs-content gc-analytics-event " track-metadata-eventdetail="https://cloud.google.com/bigquery/docs/introduction" track-type="nav" track-metadata-position="nav - guides" track-metadata-module="primary nav" aria-label="Guides, selected" data-category="Site-Wide Custom Events" data-label="Tab: Guides" track-name="guides">
    Guides
  
    </a>
    
  
          </tab>
        
      
        
          <tab>
            
    <a href="https://cloud.google.com/bigquery/quotas" class="devsite-tabs-content gc-analytics-event " track-metadata-eventdetail="https://cloud.google.com/bigquery/quotas" track-type="nav" track-metadata-position="nav - reference" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Reference" track-name="reference">
    Reference
  
    </a>
    
  
          </tab>
        
      
        
          <tab>
            
    <a href="https://cloud.google.com/bigquery/docs/samples" class="devsite-tabs-content gc-analytics-event " track-metadata-eventdetail="https://cloud.google.com/bigquery/docs/samples" track-type="nav" track-metadata-position="nav - samples" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Samples" track-name="samples">
    Samples
  
    </a>
    
  
          </tab>
        
      
        
          <tab>
            
    <a href="https://cloud.google.com/bigquery/docs/release-notes" class="devsite-tabs-content gc-analytics-event " track-metadata-eventdetail="https://cloud.google.com/bigquery/docs/release-notes" track-type="nav" track-metadata-position="nav - resources" track-metadata-module="primary nav" data-category="Site-Wide Custom Events" data-label="Tab: Resources" track-name="resources">
    Resources
  
    </a>
    
  
          </tab>
        
      
    <tab class="devsite-overflow-tab" style=""><!---->
          <button class="devsite-tabs-overflow-button devsite-icon devsite-icon-arrow-drop-down" aria-haspopup="menu" aria-expanded="false" id="tab-overflow-button-goCM" aria-label="More Options" aria-controls="tab-overflow-menu-UL3D"><!--?lit$118760000$-->More</button>
          <div class="devsite-tabs-overflow-menu" hidden="" scrollbars="" role="menu" id="tab-overflow-menu-UL3D" aria-labelledby="tab-overflow-button-goCM">
          </div>
        </tab></nav>

  <!----><button class="devsite-scroll-button devsite-scroll-right" aria-label="Scroll to more navigation items"></button><div class="devsite-overflow-cover devsite-right-overflow"></div></cloudx-tabs-nav>

          
          
            <div class="devsite-product-button-row">
  

  
  <a href="https://cloud.google.com/contact" class="cta-button-secondary button
      " track-name="sales" track-metadata-position="nav" track-type="contact" track-metadata-eventdetail="nav">Contact Us</a>

  
  <a href="//console.cloud.google.com/freetrial" class="cloud-free-trial-button button button-primary
      " referrerpolicy="no-referrer-when-downgrade" track-metadata-position="nav" track-name="gcpCta" track-type="freeTrial" track-metadata-eventdetail="nav">Start free</a>

</div>
          
        </div>
      
    </div>
  </div>

</div>



  

  
</devsite-header>
      <div class="devsite-book-nav-bg" fixed=""></div><devsite-book-nav scrollbars="" fixed="" user-scrolled="" style="--devsite-book-nav-max-height: 582.1999969482422px; top: 112.8px;">
        
          





















<div class="devsite-book-nav-filter">
  <span class="filter-list-icon material-icons" aria-hidden="true"></span>
  <input type="text" placeholder="Filter" aria-label="Type to filter" role="searchbox">
  
  <span class="filter-clear-button hidden" data-title="Clear filter" aria-label="Clear filter" role="button" tabindex="0"></span>
</div>

<nav class="devsite-book-nav devsite-nav nocontent" aria-label="Side menu">
  <div class="devsite-mobile-header">
    <button type="button" id="devsite-close-nav" class="devsite-header-icon-button button-flat material-icons gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Close navigation" aria-label="Close navigation">
    </button>
    <div class="devsite-product-name-wrapper">

  <a href="/" class="devsite-site-logo-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Site logo" track-type="globalNav" track-name="googleCloud" track-metadata-position="nav" track-metadata-eventdetail="nav">
  
  <picture>
    
    <img src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/cloud-logo.svg" class="devsite-site-logo" alt="Google Cloud">
  </picture>
  
</a>


  
      <span class="devsite-product-name">
        
        
        <ul class="devsite-breadcrumb-list">
  
  <li class="devsite-breadcrumb-item
             devsite-has-google-wordmark">
    
    
    
      
      
    
  </li>
  
</ul>
      </span>
    

</div>
  </div>

  <div class="devsite-book-nav-wrapper">
    <div class="devsite-mobile-nav-top">
      
        <ul class="devsite-nav-list">
          
            <li class="devsite-nav-item">
              
  
  <a href="/docs" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Tab: Documentation" track-name="docs-home" track-link-column-type="single-column" track-type="globalNav" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Documentation
   </span>
    
  
  </a>
  

  
              
                <ul class="devsite-nav-responsive-tabs">
                  
                    
                    
                    
                    <li class="devsite-nav-item">
                      
  
  <a href="/bigquery/docs/introduction" class="devsite-nav-title gc-analytics-event devsite-nav-has-children" data-category="Site-Wide Custom Events" data-label="Tab: Guides" track-name="guides" track-type="globalNav" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="" menu="_book">
      Guides
   </span>
    
    <span class="devsite-nav-icon material-icons" data-icon="forward" menu="_book">
    </span>
    
  
  </a>
  

  
                    </li>
                  
                    
                    
                    
                    <li class="devsite-nav-item">
                      
  
  <a href="/bigquery/quotas" class="devsite-nav-title gc-analytics-event
              devsite-nav-has-children
              " data-category="Site-Wide Custom Events" data-label="Tab: Reference" track-name="reference" track-type="globalNav" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Reference
   </span>
    
    <span class="devsite-nav-icon material-icons" data-icon="forward">
    </span>
    
  
  </a>
  

  
                    </li>
                  
                    
                    
                    
                    <li class="devsite-nav-item">
                      
  
  <a href="/bigquery/docs/samples" class="devsite-nav-title gc-analytics-event
              devsite-nav-has-children
              " data-category="Site-Wide Custom Events" data-label="Tab: Samples" track-name="samples" track-type="globalNav" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Samples
   </span>
    
    <span class="devsite-nav-icon material-icons" data-icon="forward">
    </span>
    
  
  </a>
  

  
                    </li>
                  
                    
                    
                    
                    <li class="devsite-nav-item">
                      
  
  <a href="/bigquery/docs/release-notes" class="devsite-nav-title gc-analytics-event
              devsite-nav-has-children
              " data-category="Site-Wide Custom Events" data-label="Tab: Resources" track-name="resources" track-type="globalNav" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Resources
   </span>
    
    <span class="devsite-nav-icon material-icons" data-icon="forward">
    </span>
    
  
  </a>
  

  
                    </li>
                  
                </ul>
              
            </li>
          
            <li class="devsite-nav-item">
              
  
  <a href="/docs/tech-area-overviews" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Tab: Technology areas" track-name="technology-areas" track-link-column-type="single-column" track-type="globalNav" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Technology areas
   </span>
    
  
  </a>
  

  
    <ul class="devsite-nav-responsive-tabs devsite-nav-has-menu
               ">
      
<li class="devsite-nav-item">

  
  <span class="devsite-nav-title" tooltip="" data-category="Site-Wide Custom Events" data-label="Tab: Technology areas" track-name="technology-areas" track-link-column-type="single-column">
  
    <span class="devsite-nav-text" tooltip="" menu="Technology areas">
      More
   </span>
    
    <span class="devsite-nav-icon material-icons" data-icon="forward" menu="Technology areas">
    </span>
    
  
  </span>
  

</li>

    </ul>
  
              
            </li>
          
            <li class="devsite-nav-item">
              
  
  <a href="/docs/cross-product-overviews" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Tab: Cross-product tools" track-name="crossproduct" track-link-column-type="single-column" track-type="globalNav" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Cross-product tools
   </span>
    
  
  </a>
  

  
    <ul class="devsite-nav-responsive-tabs devsite-nav-has-menu
               ">
      
<li class="devsite-nav-item">

  
  <span class="devsite-nav-title" tooltip="" data-category="Site-Wide Custom Events" data-label="Tab: Cross-product tools" track-name="crossproduct" track-link-column-type="single-column">
  
    <span class="devsite-nav-text" tooltip="" menu="Cross-product tools">
      More
   </span>
    
    <span class="devsite-nav-icon material-icons" data-icon="forward" menu="Cross-product tools">
    </span>
    
  
  </span>
  

</li>

    </ul>
  
              
            </li>
          
            <li class="devsite-nav-item">
              
  
  <a href="/" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Tab: Related sites" track-name="related-sites" track-link-column-type="single-column" track-type="globalNav" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Related sites
   </span>
    
  
  </a>
  

  
    <ul class="devsite-nav-responsive-tabs devsite-nav-has-menu
               ">
      
<li class="devsite-nav-item">

  
  <span class="devsite-nav-title" tooltip="" data-category="Site-Wide Custom Events" data-label="Tab: Related sites" track-name="related-sites" track-link-column-type="single-column">
  
    <span class="devsite-nav-text" tooltip="" menu="Related sites">
      More
   </span>
    
    <span class="devsite-nav-icon material-icons" data-icon="forward" menu="Related sites">
    </span>
    
  
  </span>
  

</li>

    </ul>
  
              
            </li>
          
          
    
    
<li class="devsite-nav-item">

  
  <a href="//console.cloud.google.com/" class="devsite-nav-title gc-analytics-event " track-type="globalNav" track-metadata-position="nav" referrerpolicy="no-referrer-when-downgrade" track-name="console" track-metadata-eventdetail="nav" data-category="Site-Wide Custom Events" data-label="Responsive Tab: Console">
  
    <span class="devsite-nav-text" tooltip="">
      Console
   </span>
    
  
  </a>
  

</li>

  
          
            
    
      
        
<li class="devsite-nav-item">

  
  <a href="/contact" class="cta-button-secondary button" track-name="sales" track-metadata-position="nav" track-type="contact" track-metadata-eventdetail="nav" data-category="Site-Wide Custom Events" data-label="Responsive Tab: Contact Us">
  
    <span class="devsite-nav-text" tooltip="">
      Contact Us
   </span>
    
  
  </a>
  

</li>

      
    
      
        
<li class="devsite-nav-item">

  
  <a href="//console.cloud.google.com/freetrial" class="cloud-free-trial-button button button-primary" referrerpolicy="no-referrer-when-downgrade" track-metadata-position="nav" track-name="gcpCta" track-type="freeTrial" track-metadata-eventdetail="nav" data-category="Site-Wide Custom Events" data-label="Responsive Tab: Start free">
  
    <span class="devsite-nav-text" tooltip="">
      Start free
   </span>
    
  
  </a>
  

</li>

      
    
  
          
        </ul>
      
    </div>
    
      <div class="devsite-mobile-nav-bottom">
        
          
          <ul class="devsite-nav-list" menu="_book">
            <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Discover</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/introduction"><span class="devsite-nav-text" tooltip="">Product overview</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">How does BigQuery work?</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/storage_overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/storage_overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/storage_overview"><span class="devsite-nav-text" tooltip="">Storage</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/query-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-overview"><span class="devsite-nav-text" tooltip="">Analytics</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/admin-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/admin-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/admin-intro"><span class="devsite-nav-text" tooltip="">Administration</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Get started</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/sandbox" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/sandbox" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/sandbox"><span class="devsite-nav-text" tooltip="">Use the BigQuery sandbox</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Quickstarts</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Try the Cloud console</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/quickstarts/query-public-dataset-console" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/quickstarts/query-public-dataset-console" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/quickstarts/query-public-dataset-console"><span class="devsite-nav-text" tooltip="">Query public data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/quickstarts/load-data-console" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/quickstarts/load-data-console" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/quickstarts/load-data-console"><span class="devsite-nav-text" tooltip="">Load and query data</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Try the command-line tool</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/quickstarts/query-public-dataset-bq" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/quickstarts/query-public-dataset-bq" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/quickstarts/query-public-dataset-bq"><span class="devsite-nav-text" tooltip="">Query public data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/quickstarts/load-data-bq" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/quickstarts/load-data-bq" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/quickstarts/load-data-bq"><span class="devsite-nav-text" tooltip="">Load and query data</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/quickstarts/quickstart-client-libraries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/quickstarts/quickstart-client-libraries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/quickstarts/quickstart-client-libraries"><span class="devsite-nav-text" tooltip="">Try the client libraries</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dataframes-quickstart" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dataframes-quickstart" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dataframes-quickstart"><span class="devsite-nav-text" tooltip="">Try DataFrames</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Explore BigQuery tools</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/bigquery-web-ui" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bigquery-web-ui" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bigquery-web-ui"><span class="devsite-nav-text" tooltip="">Explore the console</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/bq-command-line-tool" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bq-command-line-tool" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bq-command-line-tool"><span class="devsite-nav-text" tooltip="">Explore the command-line tool</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Migrate</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/migration/migration-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/migration-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/migration-overview"><span class="devsite-nav-text" tooltip="">Overview</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Migrate a data warehouse</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/migration-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration-intro"><span class="devsite-nav-text" tooltip="">Introduction to BigQuery Migration Service</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration-assessment" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration-assessment" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration-assessment"><span class="devsite-nav-text" tooltip="">Migration assessment</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/schema-data-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/schema-data-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/schema-data-overview"><span class="devsite-nav-text" tooltip="">Migrate schema and data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/pipelines" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/pipelines" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/pipelines"><span class="devsite-nav-text" tooltip="">Migrate data pipelines</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Migrate SQL</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/interactive-sql-translator" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/interactive-sql-translator" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/interactive-sql-translator"><span class="devsite-nav-text" tooltip="">Translate SQL queries interactively</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/api-sql-translator" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/api-sql-translator" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/api-sql-translator"><span class="devsite-nav-text" tooltip="">Translate SQL queries using the API</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/batch-sql-translator" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/batch-sql-translator" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/batch-sql-translator"><span class="devsite-nav-text" tooltip="">Translate SQL queries in batch</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/generate-metadata" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-metadata" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-metadata"><span class="devsite-nav-text" tooltip="">Generate metadata for translation and assessment</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/config-yaml-translation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/config-yaml-translation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/config-yaml-translation"><span class="devsite-nav-text" tooltip="">Transform SQL translations with YAML</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/output-name-mapping" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/output-name-mapping" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/output-name-mapping"><span class="devsite-nav-text" tooltip="">Map SQL object names for batch translation</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Migration guides</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Amazon Redshift</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/migration/redshift-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/redshift-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/redshift-overview"><span class="devsite-nav-text" tooltip="">Migration overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/redshift" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/redshift" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/redshift"><span class="devsite-nav-text" tooltip="">Migrate Amazon Redshift schema and data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/redshift-vpc" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/redshift-vpc" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/redshift-vpc"><span class="devsite-nav-text" tooltip="">Migrate Amazon Redshift schema and data when using a VPC</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/redshift-sql" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/redshift-sql" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/redshift-sql"><span class="devsite-nav-text" tooltip="">SQL translation reference</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Apache Hadoop</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/hadoop-metadata" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/hadoop-metadata" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/hadoop-metadata"><span class="devsite-nav-text" tooltip="">Extract metadata from Hadoop for migration</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/hadoop-permissions-migration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/hadoop-permissions-migration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/hadoop-permissions-migration"><span class="devsite-nav-text" tooltip="">Migrate permissions from Hadoop</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/hdfs-data-lake-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/hdfs-data-lake-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/hdfs-data-lake-transfer"><span class="devsite-nav-text" tooltip="">Schedule an HDFS data lake transfer</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Apache Hive</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/migration/hive-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/hive-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/hive-overview"><span class="devsite-nav-text" tooltip="">Hive migration overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/hive" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/hive" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/hive"><span class="devsite-nav-text" tooltip="">Migrate Apache Hive schema and data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/hive-sql" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/hive-sql" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/hive-sql"><span class="devsite-nav-text" tooltip="">SQL translation reference</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">IBM Netezza</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/migration/netezza" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/netezza" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/netezza"><span class="devsite-nav-text" tooltip="">Migrate from IBM Netezza</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/netezza-sql" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/netezza-sql" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/netezza-sql"><span class="devsite-nav-text" tooltip="">SQL translation reference</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Oracle</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/migration/oracle-migration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/oracle-migration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/oracle-migration"><span class="devsite-nav-text" tooltip="">Migration guide</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/oracle-sql" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/oracle-sql" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/oracle-sql"><span class="devsite-nav-text" tooltip="">SQL translation reference</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Snowflake</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/migration/snowflake-migration-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/snowflake-migration-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/snowflake-migration-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/migration/snowflake-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/snowflake-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/snowflake-transfer"><span class="devsite-nav-text" tooltip="">Schedule a Snowflake transfer</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/snowflake-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/snowflake-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/snowflake-overview"><span class="devsite-nav-text" tooltip="">Migration overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/snowflake-sql" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/snowflake-sql" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/snowflake-sql"><span class="devsite-nav-text" tooltip="">SQL translation reference</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Teradata</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/migration/teradata-migration-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/teradata-migration-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/teradata-migration-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/teradata-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/teradata-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/teradata-overview"><span class="devsite-nav-text" tooltip="">Migration overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/teradata" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/teradata" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/teradata"><span class="devsite-nav-text" tooltip="">Migrate Teradata schema and data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/teradata-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/teradata-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/teradata-tutorial"><span class="devsite-nav-text" tooltip="">Migration tutorial</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/migration/teradata-sql" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/migration/teradata-sql" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/migration/teradata-sql"><span class="devsite-nav-text" tooltip="">SQL translation reference</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Design</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/resource-hierarchy" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/resource-hierarchy" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/resource-hierarchy"><span class="devsite-nav-text" tooltip="">Organize resources</span></a></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/service-dependencies" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/service-dependencies" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/service-dependencies"><span class="devsite-nav-text" tooltip="">API dependencies</span></a></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/editions-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/editions-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/editions-intro"><span class="devsite-nav-text" tooltip="">Understand editions</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Datasets</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/datasets-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/datasets-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/datasets-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/datasets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/datasets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/datasets"><span class="devsite-nav-text" tooltip="">Create datasets</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/listing-datasets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/listing-datasets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/listing-datasets"><span class="devsite-nav-text" tooltip="">List datasets</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-replication" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-replication" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-replication"><span class="devsite-nav-text" tooltip="">Cross-region replication</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/managed-disaster-recovery" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managed-disaster-recovery" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managed-disaster-recovery"><span class="devsite-nav-text" tooltip="">Managed disaster recovery</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/disaster-recovery-migration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/disaster-recovery-migration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/disaster-recovery-migration"><span class="devsite-nav-text" tooltip="">Migrate to managed disaster recovery</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/time-travel" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/time-travel" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/time-travel"><span class="devsite-nav-text" tooltip="">Dataset data retention</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav expanded">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Tables</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav expanded">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Big<wbr>Query tables</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/tables-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/tables-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/tables-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/tables"><span class="devsite-nav-text" tooltip="">Create and use tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/iceberg-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/iceberg-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/iceberg-tables"><span class="devsite-nav-text" tooltip="">Big<wbr>Lake Iceberg tables in Big<wbr>Query</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Specify table schemas</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/schemas" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/schemas" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/schemas"><span class="devsite-nav-text" tooltip="">Specify a schema</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/nested-repeated" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/nested-repeated" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/nested-repeated"><span class="devsite-nav-text" tooltip="">Specify nested and repeated columns</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/default-values" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/default-values" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/default-values"><span class="devsite-nav-text" tooltip="">Specify default column values</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/objectref-columns" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/objectref-columns" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/objectref-columns"><span class="devsite-nav-text" tooltip="">Specify ObjectRef values</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav expanded">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Segment with partitioned tables</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/partitioned-tables" class="devsite-nav-title gc-analytics-event devsite-nav-active" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/partitioned-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/partitioned-tables" aria-selected="true"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/creating-partitioned-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/creating-partitioned-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/creating-partitioned-tables"><span class="devsite-nav-text" tooltip="">Create partitioned tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/managing-partitioned-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-partitioned-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-partitioned-tables"><span class="devsite-nav-text" tooltip="">Manage partitioned tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/querying-partitioned-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/querying-partitioned-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/querying-partitioned-tables"><span class="devsite-nav-text" tooltip="">Query partitioned tables</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Optimize with clustered tables</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/clustered-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/clustered-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/clustered-tables"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/creating-clustered-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/creating-clustered-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/creating-clustered-tables"><span class="devsite-nav-text" tooltip="">Create clustered tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/manage-clustered-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/manage-clustered-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/manage-clustered-tables"><span class="devsite-nav-text" tooltip="">Manage clustered tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/querying-clustered-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/querying-clustered-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/querying-clustered-tables"><span class="devsite-nav-text" tooltip="">Query clustered tables</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/metadata-indexing-managed-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/metadata-indexing-managed-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/metadata-indexing-managed-tables"><span class="devsite-nav-text" tooltip="">Use metadata indexing</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">External tables</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/external-data-sources" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/external-data-sources" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/external-data-sources"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Types of external tables</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/biglake-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/biglake-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/biglake-intro"><span class="devsite-nav-text" tooltip="">BigLake external tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/omni-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/omni-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/omni-introduction"><span class="devsite-nav-text" tooltip="">BigQuery Omni</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/object-table-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/object-table-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/object-table-introduction"><span class="devsite-nav-text" tooltip="">Object tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/external-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/external-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/external-tables"><span class="devsite-nav-text" tooltip="">External tables</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/external-table-definition" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/external-table-definition" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/external-table-definition"><span class="devsite-nav-text" tooltip="">External table definition file</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/hive-partitioned-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/hive-partitioned-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/hive-partitioned-queries"><span class="devsite-nav-text" tooltip="">Externally partitioned data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/metadata-caching-external-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/metadata-caching-external-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/metadata-caching-external-tables"><span class="devsite-nav-text" tooltip="">Use metadata caching</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/omni-aws-create-external-table" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/omni-aws-create-external-table" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/omni-aws-create-external-table"><span class="devsite-nav-text" tooltip="">Amazon S3 BigLake external tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/iceberg-external-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/iceberg-external-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/iceberg-external-tables"><span class="devsite-nav-text" tooltip="">Apache Iceberg external tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/omni-azure-create-external-table" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/omni-azure-create-external-table" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/omni-azure-create-external-table"><span class="devsite-nav-text" tooltip="">Azure Blob Storage BigLake tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/create-bigtable-external-table" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-bigtable-external-table" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-bigtable-external-table"><span class="devsite-nav-text" tooltip="">Bigtable external table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/create-cloud-storage-table-biglake" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-cloud-storage-table-biglake" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-cloud-storage-table-biglake"><span class="devsite-nav-text" tooltip="">BigLake external tables for Cloud Storage</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/object-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/object-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/object-tables"><span class="devsite-nav-text" tooltip="">Cloud Storage object tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/external-data-cloud-storage" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/external-data-cloud-storage" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/external-data-cloud-storage"><span class="devsite-nav-text" tooltip="">Cloud Storage external tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/create-delta-lake-table" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-delta-lake-table" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-delta-lake-table"><span class="devsite-nav-text" tooltip="">Delta Lake BigLake tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/external-data-drive" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/external-data-drive" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/external-data-drive"><span class="devsite-nav-text" tooltip="">Google Drive external tables</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Views</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Logical views</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/views-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/views-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/views-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/views" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/views" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/views"><span class="devsite-nav-text" tooltip="">Create logical views</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Materialized views</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/materialized-views-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/materialized-views-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/materialized-views-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/materialized-views-create" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/materialized-views-create" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/materialized-views-create"><span class="devsite-nav-text" tooltip="">Create materialized views</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/materialized-view-replicas-create" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/materialized-view-replicas-create" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/materialized-view-replicas-create"><span class="devsite-nav-text" tooltip="">Create materialized view replicas</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage all view types</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/view-metadata" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/view-metadata" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/view-metadata"><span class="devsite-nav-text" tooltip="">Get information about views</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/managing-views" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-views" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-views"><span class="devsite-nav-text" tooltip="">Manage views</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Routines</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/routines-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/routines-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/routines-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/routines" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/routines" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/routines"><span class="devsite-nav-text" tooltip="">Manage routines</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/user-defined-functions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/user-defined-functions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/user-defined-functions"><span class="devsite-nav-text" tooltip="">User-defined functions</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/user-defined-functions-python" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/user-defined-functions-python" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/user-defined-functions-python"><span class="devsite-nav-text" tooltip="">User-defined functions in Python</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/user-defined-aggregates" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/user-defined-aggregates" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/user-defined-aggregates"><span class="devsite-nav-text" tooltip="">User-defined aggregate functions</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-functions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-functions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-functions"><span class="devsite-nav-text" tooltip="">Table functions</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/remote-functions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/remote-functions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/remote-functions"><span class="devsite-nav-text" tooltip="">Remote functions</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/procedures" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/procedures" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/procedures"><span class="devsite-nav-text" tooltip="">SQL stored procedures</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/spark-procedures" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/spark-procedures" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/spark-procedures"><span class="devsite-nav-text" tooltip="">Stored procedures for Apache Spark</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/object-table-remote-function" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/object-table-remote-function" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/object-table-remote-function"><span class="devsite-nav-text" tooltip="">Analyze object tables by using remote functions</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/remote-functions-translation-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/remote-functions-translation-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/remote-functions-translation-tutorial"><span class="devsite-nav-text" tooltip="">Remote functions and Translation API tutorial</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Connections</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/connections-api-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/connections-api-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/connections-api-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/omni-aws-create-connection" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/omni-aws-create-connection" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/omni-aws-create-connection"><span class="devsite-nav-text" tooltip="">Amazon S3 connection</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/connect-to-spark" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/connect-to-spark" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/connect-to-spark"><span class="devsite-nav-text" tooltip="">Apache Spark connection</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/omni-azure-create-connection" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/omni-azure-create-connection" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/omni-azure-create-connection"><span class="devsite-nav-text" tooltip="">Azure Blob Storage connection</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/create-cloud-resource-connection" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-cloud-resource-connection" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-cloud-resource-connection"><span class="devsite-nav-text" tooltip="">Cloud resource connection</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/connect-to-spanner" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/connect-to-spanner" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/connect-to-spanner"><span class="devsite-nav-text" tooltip="">Spanner connection</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/connect-to-sql" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/connect-to-sql" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/connect-to-sql"><span class="devsite-nav-text" tooltip="">Cloud SQL connection</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/connect-to-alloydb" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/connect-to-alloydb" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/connect-to-alloydb"><span class="devsite-nav-text" tooltip="">AlloyDB connection</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/connect-to-sap-datasphere" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/connect-to-sap-datasphere" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/connect-to-sap-datasphere"><span class="devsite-nav-text" tooltip="">SAP Datasphere connection</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/working-with-connections" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/working-with-connections" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/working-with-connections"><span class="devsite-nav-text" tooltip="">Manage connections</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/connections-with-network-attachment" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/connections-with-network-attachment" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/connections-with-network-attachment"><span class="devsite-nav-text" tooltip="">Configure connections with network attachments</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/default-connections" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/default-connections" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/default-connections"><span class="devsite-nav-text" tooltip="">Default connections</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Indexes</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Search indexes</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/search-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/search-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/search-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/search-index" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/search-index" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/search-index"><span class="devsite-nav-text" tooltip="">Manage search indexes</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Vector indexes</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/vector-search-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/vector-search-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/vector-search-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/vector-index" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/vector-index" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/vector-index"><span class="devsite-nav-text" tooltip="">Manage vector indexes</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Load,<wbr> transform,<wbr> and export</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/load-transform-export-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/load-transform-export-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/load-transform-export-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Load data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/loading-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/loading-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/loading-data"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">BigQuery Data Transfer Service</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/dts-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dts-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dts-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dts-locations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dts-locations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dts-locations"><span class="devsite-nav-text" tooltip="">Data location and transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dts-authentication-authorization" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dts-authentication-authorization" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dts-authentication-authorization"><span class="devsite-nav-text" tooltip="">Authorize transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/enable-transfer-service" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/enable-transfer-service" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/enable-transfer-service"><span class="devsite-nav-text" tooltip="">Enable transfers</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Set up network connections</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/cloud-sql-instance-access" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/cloud-sql-instance-access" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/cloud-sql-instance-access"><span class="devsite-nav-text" tooltip="">Cloud SQL instance access</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/aws-vpn-network-attachment" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/aws-vpn-network-attachment" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/aws-vpn-network-attachment"><span class="devsite-nav-text" tooltip="">AWS VPN and network attachment</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/azure-vpn-network-attachment" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/azure-vpn-network-attachment" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/azure-vpn-network-attachment"><span class="devsite-nav-text" tooltip="">Azure VPN and network attachment</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/working-with-transfers" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/working-with-transfers" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/working-with-transfers"><span class="devsite-nav-text" tooltip="">Manage transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/transfer-run-notifications" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/transfer-run-notifications" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/transfer-run-notifications"><span class="devsite-nav-text" tooltip="">Transfer run notifications</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/transfer-troubleshooting" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/transfer-troubleshooting" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/transfer-troubleshooting"><span class="devsite-nav-text" tooltip="">Troubleshoot transfer configurations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/use-service-accounts" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/use-service-accounts" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/use-service-accounts"><span class="devsite-nav-text" tooltip="">Use service accounts</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/third-party-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/third-party-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/third-party-transfer"><span class="devsite-nav-text" tooltip="">Use third-party transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/transfer-custom-constraints" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/transfer-custom-constraints" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/transfer-custom-constraints"><span class="devsite-nav-text" tooltip="">Use custom organization policies</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/transfer-changes" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/transfer-changes" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/transfer-changes"><span class="devsite-nav-text" tooltip="">Data source change log</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/event-driven-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/event-driven-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/event-driven-transfer"><span class="devsite-nav-text" tooltip="">Event-driven transfers</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Transfer guides</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Amazon S3</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/s3-transfer-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/s3-transfer-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/s3-transfer-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/s3-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/s3-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/s3-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/s3-transfer-parameters" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/s3-transfer-parameters" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/s3-transfer-parameters"><span class="devsite-nav-text" tooltip="">Transfer runtime parameters</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Azure Blob Storage</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/blob-storage-transfer-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blob-storage-transfer-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blob-storage-transfer-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blob-storage-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blob-storage-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blob-storage-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blob-storage-transfer-parameters" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blob-storage-transfer-parameters" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blob-storage-transfer-parameters"><span class="devsite-nav-text" tooltip="">Transfer runtime parameters</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Campaign Manager</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/doubleclick-campaign-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/doubleclick-campaign-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/doubleclick-campaign-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/doubleclick-campaign-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/doubleclick-campaign-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/doubleclick-campaign-transformation"><span class="devsite-nav-text" tooltip="">Report transformation</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Cloud Storage</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/cloud-storage-transfer-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/cloud-storage-transfer-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/cloud-storage-transfer-overview"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/cloud-storage-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/cloud-storage-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/cloud-storage-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/gcs-transfer-parameters" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/gcs-transfer-parameters" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/gcs-transfer-parameters"><span class="devsite-nav-text" tooltip="">Transfer runtime parameters</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Comparison Shopping Service Center</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/css-center-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/css-center-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/css-center-transfer"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/css-center-transfer-schedule-transfers" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/css-center-transfer-schedule-transfers" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/css-center-transfer-schedule-transfers"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/css-center-products-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/css-center-products-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/css-center-products-schema"><span class="devsite-nav-text" tooltip="">Transfer report schema</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Display &amp; Video 360</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/display-video-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/display-video-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/display-video-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/display-video-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/display-video-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/display-video-transformation"><span class="devsite-nav-text" tooltip="">Report transformation</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Facebook Ads</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/facebook-ads-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/facebook-ads-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/facebook-ads-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/facebook-ads-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/facebook-ads-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/facebook-ads-transformation"><span class="devsite-nav-text" tooltip="">Report transformation</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Google Ad Manager</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/doubleclick-publisher-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/doubleclick-publisher-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/doubleclick-publisher-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/doubleclick-publisher-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/doubleclick-publisher-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/doubleclick-publisher-transformation"><span class="devsite-nav-text" tooltip="">Report transformation</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Google Ads</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/google-ads-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/google-ads-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/google-ads-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/google-ads-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/google-ads-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/google-ads-transformation"><span class="devsite-nav-text" tooltip="">Report transformation</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Google Analytics 4</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/google-analytics-4-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/google-analytics-4-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/google-analytics-4-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/google-analytics-4-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/google-analytics-4-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/google-analytics-4-transformation"><span class="devsite-nav-text" tooltip="">Report transformation</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Google Merchant Center</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-transfer"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-transfer-schedule-transfers" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-transfer-schedule-transfers" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-transfer-schedule-transfers"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-query-your-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-query-your-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-query-your-data"><span class="devsite-nav-text" tooltip="">Query your data</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Migration guides</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-best-sellers-migration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-best-sellers-migration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-best-sellers-migration"><span class="devsite-nav-text" tooltip="">Best sellers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-price-competitiveness-migration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-price-competitiveness-migration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-price-competitiveness-migration"><span class="devsite-nav-text" tooltip="">Price competitiveness</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Transfer report schema</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-best-sellers-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-best-sellers-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-best-sellers-schema"><span class="devsite-nav-text" tooltip="">Best Sellers table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-local-inventories-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-local-inventories-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-local-inventories-schema"><span class="devsite-nav-text" tooltip="">Local Inventories table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-performance-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-performance-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-performance-schema"><span class="devsite-nav-text" tooltip="">Performance table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-price-benchmarks-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-price-benchmarks-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-price-benchmarks-schema"><span class="devsite-nav-text" tooltip="">Price Benchmarks table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-price-competitiveness-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-price-competitiveness-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-price-competitiveness-schema"><span class="devsite-nav-text" tooltip="">Price Competitiveness table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-price-insights-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-price-insights-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-price-insights-schema"><span class="devsite-nav-text" tooltip="">Price Insights table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-product-inventory-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-product-inventory-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-product-inventory-schema"><span class="devsite-nav-text" tooltip="">Product Inventory table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-product-targeting-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-product-targeting-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-product-targeting-schema"><span class="devsite-nav-text" tooltip="">Product Targeting table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-products-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-products-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-products-schema"><span class="devsite-nav-text" tooltip="">Products table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-regional-inventories-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-regional-inventories-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-regional-inventories-schema"><span class="devsite-nav-text" tooltip="">Regional Inventories table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-top-brands-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-top-brands-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-top-brands-schema"><span class="devsite-nav-text" tooltip="">Top Brands table</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/merchant-center-top-products-schema" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/merchant-center-top-products-schema" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/merchant-center-top-products-schema"><span class="devsite-nav-text" tooltip="">Top Products table</span></a></li></ul></div></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Google Play</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/play-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/play-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/play-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/play-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/play-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/play-transformation"><span class="devsite-nav-text" tooltip="">Transfer report transformation</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">MySQL</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/mysql-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/mysql-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/mysql-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Oracle</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/oracle-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/oracle-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/oracle-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">PostgreSQL</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/postgresql-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/postgresql-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/postgresql-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Salesforce</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/salesforce-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/salesforce-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/salesforce-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Salesforce Marketing Cloud</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/sfmc-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/sfmc-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/sfmc-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Search Ads 360</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/search-ads-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/search-ads-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/search-ads-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/search-ads-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/search-ads-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/search-ads-transformation"><span class="devsite-nav-text" tooltip="">Transfer report transformation</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/search-ads-migration-guide" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/search-ads-migration-guide" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/search-ads-migration-guide"><span class="devsite-nav-text" tooltip="">Migration guide</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">ServiceNow</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/servicenow-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/servicenow-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/servicenow-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">YouTube channel</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/youtube-channel-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/youtube-channel-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/youtube-channel-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/youtube-channel-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/youtube-channel-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/youtube-channel-transformation"><span class="devsite-nav-text" tooltip="">Transfer report transformation</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">YouTube content owner</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/youtube-content-owner-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/youtube-content-owner-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/youtube-content-owner-transfer"><span class="devsite-nav-text" tooltip="">Schedule transfers</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/youtube-content-owner-transformation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/youtube-content-owner-transformation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/youtube-content-owner-transformation"><span class="devsite-nav-text" tooltip="">Transfer report transformation</span></a></li></ul></div></li></ul></div></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Batch load data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/batch-loading-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/batch-loading-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/batch-loading-data"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/schema-detect" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/schema-detect" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/schema-detect"><span class="devsite-nav-text" tooltip="">Auto-detect schemas</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/loading-data-cloud-storage-avro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/loading-data-cloud-storage-avro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/loading-data-cloud-storage-avro"><span class="devsite-nav-text" tooltip="">Load Avro data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/loading-data-cloud-storage-parquet" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/loading-data-cloud-storage-parquet" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/loading-data-cloud-storage-parquet"><span class="devsite-nav-text" tooltip="">Load Parquet data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/loading-data-cloud-storage-orc" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/loading-data-cloud-storage-orc" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/loading-data-cloud-storage-orc"><span class="devsite-nav-text" tooltip="">Load ORC data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/loading-data-cloud-storage-csv" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/loading-data-cloud-storage-csv" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/loading-data-cloud-storage-csv"><span class="devsite-nav-text" tooltip="">Load CSV data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/loading-data-cloud-storage-json" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/loading-data-cloud-storage-json" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/loading-data-cloud-storage-json"><span class="devsite-nav-text" tooltip="">Load JSON data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/hive-partitioned-loads-gcs" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/hive-partitioned-loads-gcs" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/hive-partitioned-loads-gcs"><span class="devsite-nav-text" tooltip="">Load externally partitioned data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/loading-data-cloud-datastore" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/loading-data-cloud-datastore" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/loading-data-cloud-datastore"><span class="devsite-nav-text" tooltip="">Load data from a Datastore export</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/loading-data-cloud-firestore" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/loading-data-cloud-firestore" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/loading-data-cloud-firestore"><span class="devsite-nav-text" tooltip="">Load data from a Firestore export</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/write-api-batch-load" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/write-api-batch-load" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/write-api-batch-load"><span class="devsite-nav-text" tooltip="">Load data using the Storage Write API</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/load-data-partitioned-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/load-data-partitioned-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/load-data-partitioned-tables"><span class="devsite-nav-text" tooltip="">Load data into partitioned tables</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Write and read data with the Storage API</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/reference/storage" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reference/storage" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reference/storage"><span class="devsite-nav-text" tooltip="">Read data with the Storage Read API</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Write data with the Storage Write API</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/write-api" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/write-api" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/write-api"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/write-api-streaming" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/write-api-streaming" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/write-api-streaming"><span class="devsite-nav-text" tooltip="">Stream data with the Storage Write API</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/write-api-batch" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/write-api-batch" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/write-api-batch"><span class="devsite-nav-text" tooltip="">Batch load data with the Storage Write API</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/write-api-best-practices" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/write-api-best-practices" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/write-api-best-practices"><span class="devsite-nav-text" tooltip="">Best practices</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/supported-data-types" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/supported-data-types" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/supported-data-types"><span class="devsite-nav-text" tooltip="">Supported protocol buffer and Arrow data types</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/change-data-capture" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/change-data-capture" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/change-data-capture"><span class="devsite-nav-text" tooltip="">Stream updates with change data capture</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/streaming-data-into-bigquery" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/streaming-data-into-bigquery" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/streaming-data-into-bigquery"><span class="devsite-nav-text" tooltip="">Use the legacy streaming API</span></a></li></ul></div></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/load-data-google-services" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/load-data-google-services" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/load-data-google-services"><span class="devsite-nav-text" tooltip="">Load data from other Google services</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/automatic-discovery" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/automatic-discovery" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/automatic-discovery"><span class="devsite-nav-text" tooltip="">Discover and catalog Cloud Storage data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/load-data-third-party" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/load-data-third-party" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/load-data-third-party"><span class="devsite-nav-text" tooltip="">Load data using third-party apps</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/load-data-using-cross-cloud-transfer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/load-data-using-cross-cloud-transfer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/load-data-using-cross-cloud-transfer"><span class="devsite-nav-text" tooltip="">Load data using cross-cloud operations</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Transform data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/transform-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/transform-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/transform-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Prepare data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/data-prep-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-prep-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-prep-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-prep-get-suggestions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-prep-get-suggestions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-prep-get-suggestions"><span class="devsite-nav-text" tooltip="">Prepare data with Gemini</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-manipulation-language" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-manipulation-language" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-manipulation-language"><span class="devsite-nav-text" tooltip="">Transform with DML</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/using-dml-with-partitioned-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/using-dml-with-partitioned-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/using-dml-with-partitioned-tables"><span class="devsite-nav-text" tooltip="">Transform data in partitioned tables</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/change-history" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/change-history" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/change-history"><span class="devsite-nav-text" tooltip="">Work with change history</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Transform data with pipelines</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/pipelines-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/pipelines-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/pipelines-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/create-pipelines" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-pipelines" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-pipelines"><span class="devsite-nav-text" tooltip="">Create pipelines</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Export data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/export-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/export-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/export-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/export-file" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/export-file" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/export-file"><span class="devsite-nav-text" tooltip="">Export query results</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/exporting-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/exporting-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/exporting-data"><span class="devsite-nav-text" tooltip="">Export to Cloud Storage</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/export-to-bigtable" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/export-to-bigtable" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/export-to-bigtable"><span class="devsite-nav-text" tooltip="">Export to Bigtable</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/export-to-spanner" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/export-to-spanner" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/export-to-spanner"><span class="devsite-nav-text" tooltip="">Export to Spanner</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/export-to-pubsub" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/export-to-pubsub" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/export-to-pubsub"><span class="devsite-nav-text" tooltip="">Export to Pub/Sub</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/protobuf-export" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/protobuf-export" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/protobuf-export"><span class="devsite-nav-text" tooltip="">Export as Protobuf columns</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Analyze</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/query-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-overview"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/search-resources" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/search-resources" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/search-resources"><span class="devsite-nav-text" tooltip="">Search for resources</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Explore your data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/table-explorer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-explorer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-explorer"><span class="devsite-nav-text" tooltip="">Create queries with table explorer</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-profile-scan" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-profile-scan" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-profile-scan"><span class="devsite-nav-text" tooltip="">Profile your data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-insights" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-insights" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-insights"><span class="devsite-nav-text" tooltip="">Generate data insights</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-canvas" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-canvas" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-canvas"><span class="devsite-nav-text" tooltip="">Analyze with a data canvas</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/gemini-analyze-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/gemini-analyze-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/gemini-analyze-data"><span class="devsite-nav-text" tooltip="">Analyze data with Gemini</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Query BigQuery data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/running-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/running-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/running-queries"><span class="devsite-nav-text" tooltip="">Run a query</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/write-sql-gemini" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/write-sql-gemini" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/write-sql-gemini"><span class="devsite-nav-text" tooltip="">Write queries with Gemini</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/writing-results" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/writing-results" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/writing-results"><span class="devsite-nav-text" tooltip="">Write query results</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Query data with SQL</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/introduction-sql" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/introduction-sql" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/introduction-sql"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/arrays" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/arrays" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/arrays"><span class="devsite-nav-text" tooltip="">Arrays</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/json-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/json-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/json-data"><span class="devsite-nav-text" tooltip="">JSON data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/multi-statement-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/multi-statement-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/multi-statement-queries"><span class="devsite-nav-text" tooltip="">Multi-statement queries</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/parameterized-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/parameterized-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/parameterized-queries"><span class="devsite-nav-text" tooltip="">Parameterized queries</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/pipe-syntax-guide" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/pipe-syntax-guide" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/pipe-syntax-guide"><span class="devsite-nav-text" tooltip="">Pipe syntax</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analyze-data-pipe-syntax" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analyze-data-pipe-syntax" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analyze-data-pipe-syntax"><span class="devsite-nav-text" tooltip="">Analyze data using pipe syntax</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/recursive-ctes" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/recursive-ctes" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/recursive-ctes"><span class="devsite-nav-text" tooltip="">Recursive CTEs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/sketches" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/sketches" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/sketches"><span class="devsite-nav-text" tooltip="">Sketches</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/table-sampling" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-sampling" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-sampling"><span class="devsite-nav-text" tooltip="">Table sampling</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/working-with-time-series" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/working-with-time-series" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/working-with-time-series"><span class="devsite-nav-text" tooltip="">Time series</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/transactions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/transactions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/transactions"><span class="devsite-nav-text" tooltip="">Transactions</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/querying-wildcard-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/querying-wildcard-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/querying-wildcard-tables"><span class="devsite-nav-text" tooltip="">Wildcard tables</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use geospatial analytics</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/geospatial-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/geospatial-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/geospatial-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/geospatial-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/geospatial-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/geospatial-data"><span class="devsite-nav-text" tooltip="">Work with geospatial analytics</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/raster-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/raster-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/raster-data"><span class="devsite-nav-text" tooltip="">Work with raster data</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-spatial-analysis" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-spatial-analysis" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-spatial-analysis"><span class="devsite-nav-text" tooltip="">Best practices for spatial analysis</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/geospatial-visualize" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/geospatial-visualize" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/geospatial-visualize"><span class="devsite-nav-text" tooltip="">Visualize geospatial data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/grid-systems-spatial-analysis" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/grid-systems-spatial-analysis" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/grid-systems-spatial-analysis"><span class="devsite-nav-text" tooltip="">Grid systems for spatial analysis</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reference/standard-sql/geography_functions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reference/standard-sql/geography_functions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reference/standard-sql/geography_functions"><span class="devsite-nav-text" tooltip="">Geospatial analytics syntax reference</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Geospatial analytics tutorials</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/geospatial-get-started" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/geospatial-get-started" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/geospatial-get-started"><span class="devsite-nav-text" tooltip="">Get started with geospatial analytics</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/geospatial-tutorial-hurricane" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/geospatial-tutorial-hurricane" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/geospatial-tutorial-hurricane"><span class="devsite-nav-text" tooltip="">Use geospatial analytics to plot a hurricane's path</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/geospatial-visualize-colab" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/geospatial-visualize-colab" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/geospatial-visualize-colab"><span class="devsite-nav-text" tooltip="">Visualize geospatial analytics data in a Colab notebook</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/raster-tutorial-weather" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/raster-tutorial-weather" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/raster-tutorial-weather"><span class="devsite-nav-text" tooltip="">Use raster data to analyze temperature</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Search data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/search" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/search" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/search"><span class="devsite-nav-text" tooltip="">Search indexed data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/text-analysis-search" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/text-analysis-search" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/text-analysis-search"><span class="devsite-nav-text" tooltip="">Work with text analyzers</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/access-historical-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/access-historical-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/access-historical-data"><span class="devsite-nav-text" tooltip="">Access historical data</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Work with queries</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Save queries</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/saved-queries-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/saved-queries-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/saved-queries-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/work-with-saved-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/work-with-saved-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/work-with-saved-queries"><span class="devsite-nav-text" tooltip="">Create saved queries</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Continuous queries</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/continuous-queries-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/continuous-queries-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/continuous-queries-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/continuous-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/continuous-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/continuous-queries"><span class="devsite-nav-text" tooltip="">Create continuous queries</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/cached-results" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/cached-results" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/cached-results"><span class="devsite-nav-text" tooltip="">Use cached results</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use sessions</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/sessions-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/sessions-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/sessions-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/sessions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/sessions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/sessions"><span class="devsite-nav-text" tooltip="">Work with sessions</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/sessions-write-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/sessions-write-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/sessions-write-queries"><span class="devsite-nav-text" tooltip="">Write queries in sessions</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/troubleshoot-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/troubleshoot-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/troubleshoot-queries"><span class="devsite-nav-text" tooltip="">Troubleshoot queries</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Optimize queries</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-performance-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-performance-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-performance-overview"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/query-plan-explanation" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-plan-explanation" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-plan-explanation"><span class="devsite-nav-text" tooltip="">Use the query plan explanation</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/query-insights" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-insights" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-insights"><span class="devsite-nav-text" tooltip="">Get query performance insights</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-performance-compute" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-performance-compute" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-performance-compute"><span class="devsite-nav-text" tooltip="">Optimize query computation</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/history-based-optimizations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/history-based-optimizations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/history-based-optimizations"><span class="devsite-nav-text" tooltip="">Use history-based optimizations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-storage" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-storage" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-storage"><span class="devsite-nav-text" tooltip="">Optimize storage for query performance</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/materialized-views-use" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/materialized-views-use" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/materialized-views-use"><span class="devsite-nav-text" tooltip="">Use materialized views</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/bi-engine-query" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bi-engine-query" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bi-engine-query"><span class="devsite-nav-text" tooltip="">Use BI Engine</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-performance-nested" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-performance-nested" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-performance-nested"><span class="devsite-nav-text" tooltip="">Use nested and repeated data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-performance-functions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-performance-functions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-performance-functions"><span class="devsite-nav-text" tooltip="">Optimize functions</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/advanced-runtime" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/advanced-runtime" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/advanced-runtime"><span class="devsite-nav-text" tooltip="">Use the advanced runtime</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/primary-foreign-keys" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/primary-foreign-keys" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/primary-foreign-keys"><span class="devsite-nav-text" tooltip="">Use primary and foreign keys</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Analyze multimodal data</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/analyze-multimodal-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analyze-multimodal-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analyze-multimodal-data"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/multimodal-data-sql-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/multimodal-data-sql-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/multimodal-data-sql-tutorial"><span class="devsite-nav-text" tooltip="">Analyze multimodal data with SQL and Python UDFs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/multimodal-data-dataframes-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/multimodal-data-dataframes-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/multimodal-data-dataframes-tutorial"><span class="devsite-nav-text" tooltip="">Analyze multimodal data with BigQuery DataFrames</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Query external data sources</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage open source metadata with BigLake metastore</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/about-blms" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/about-blms" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/about-blms"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blms-use-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-use-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-use-tables"><span class="devsite-nav-text" tooltip="">Use with tables in BigQuery</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/use-spark" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/use-spark" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/use-spark"><span class="devsite-nav-text" tooltip="">Use with Spark in BigQuery notebooks</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blms-use-dataproc" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-use-dataproc" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-use-dataproc"><span class="devsite-nav-text" tooltip="">Use with Dataproc</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blms-use-dataproc-serverless" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-use-dataproc-serverless" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-use-dataproc-serverless"><span class="devsite-nav-text" tooltip="">Use with Dataproc Serverless</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blms-use-stored-procedures" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-use-stored-procedures" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-use-stored-procedures"><span class="devsite-nav-text" tooltip="">Use with Spark stored procedures</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blms-manage-resources" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-manage-resources" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-manage-resources"><span class="devsite-nav-text" tooltip="">Manage Iceberg resources</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blms-query-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-query-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-query-tables"><span class="devsite-nav-text" tooltip="">Create and query tables from Spark</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blms-features" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-features" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-features"><span class="devsite-nav-text" tooltip="">Customize with additional features</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/blms-rest-catalog" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-rest-catalog" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-rest-catalog"><span class="devsite-nav-text" tooltip="">Use with the Iceberg REST catalog</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/blms-dpms-migration-tool" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/blms-dpms-migration-tool" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/blms-dpms-migration-tool"><span class="devsite-nav-text" tooltip="">Migrate from Dataproc Metastore</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/lakehouse-recommendations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/lakehouse-recommendations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/lakehouse-recommendations"><span class="devsite-nav-text" tooltip="">Optimal data and metadata formats for lakehouses</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use external tables and datasets</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Amazon S3 data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/query-aws-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-aws-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-aws-data"><span class="devsite-nav-text" tooltip="">Query Amazon S3 data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/omni-aws-export-results-to-s3" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/omni-aws-export-results-to-s3" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/omni-aws-export-results-to-s3"><span class="devsite-nav-text" tooltip="">Export query results to Amazon S3</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/query-iceberg-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-iceberg-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-iceberg-data"><span class="devsite-nav-text" tooltip="">Query Apache Iceberg data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/query-open-table-format-using-manifest-files" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-open-table-format-using-manifest-files" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-open-table-format-using-manifest-files"><span class="devsite-nav-text" tooltip="">Query open table formats with manifests</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Azure Blob Storage data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/query-azure-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-azure-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-azure-data"><span class="devsite-nav-text" tooltip="">Query Azure Blob Storage data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/omni-azure-export-results-to-azure-storage" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/omni-azure-export-results-to-azure-storage" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/omni-azure-export-results-to-azure-storage"><span class="devsite-nav-text" tooltip="">Export query results to Azure Blob Storage</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/external-data-bigtable" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/external-data-bigtable" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/external-data-bigtable"><span class="devsite-nav-text" tooltip="">Query Cloud Bigtable data</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Cloud Storage data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/query-cloud-storage-using-biglake" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-cloud-storage-using-biglake" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-cloud-storage-using-biglake"><span class="devsite-nav-text" tooltip="">Query Cloud Storage data in BigLake tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/query-cloud-storage-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-cloud-storage-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-cloud-storage-data"><span class="devsite-nav-text" tooltip="">Query Cloud Storage data in external tables</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/salesforce-quickstart" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/salesforce-quickstart" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/salesforce-quickstart"><span class="devsite-nav-text" tooltip="">Work with Salesforce Data Cloud data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/query-drive-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-drive-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-drive-data"><span class="devsite-nav-text" tooltip="">Query Google Drive data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/glue-federated-datasets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/glue-federated-datasets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/glue-federated-datasets"><span class="devsite-nav-text" tooltip="">Create AWS Glue federated datasets</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/spanner-external-datasets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/spanner-external-datasets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/spanner-external-datasets"><span class="devsite-nav-text" tooltip="">Create Spanner external datasets</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Run federated queries</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/federated-queries-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/federated-queries-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/federated-queries-intro"><span class="devsite-nav-text" tooltip="">Federated queries</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/sap-datasphere-federated-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/sap-datasphere-federated-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/sap-datasphere-federated-queries"><span class="devsite-nav-text" tooltip="">Query SAP Datasphere data</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/alloydb-federated-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/alloydb-federated-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/alloydb-federated-queries"><span class="devsite-nav-text" tooltip="">Query AlloyDB data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/spanner-federated-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/spanner-federated-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/spanner-federated-queries"><span class="devsite-nav-text" tooltip="">Query Spanner data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/cloud-sql-federated-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/cloud-sql-federated-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/cloud-sql-federated-queries"><span class="devsite-nav-text" tooltip="">Query Cloud SQL data</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use notebooks</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/programmatic-analysis" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/programmatic-analysis" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/programmatic-analysis"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use Colab notebooks</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/notebooks-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/notebooks-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/notebooks-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/create-notebooks" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-notebooks" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-notebooks"><span class="devsite-nav-text" tooltip="">Create notebooks</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/explore-data-colab" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/explore-data-colab" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/explore-data-colab"><span class="devsite-nav-text" tooltip="">Explore query results</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/use-spark" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/use-spark" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/use-spark"><span class="devsite-nav-text" tooltip="">Use Spark</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/colab-data-science-agent" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/colab-data-science-agent" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/colab-data-science-agent"><span class="devsite-nav-text" tooltip="">Use Colab Data Science Agent</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use DataFrames</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/bigquery-dataframes-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bigquery-dataframes-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bigquery-dataframes-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/use-bigquery-dataframes" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/use-bigquery-dataframes" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/use-bigquery-dataframes"><span class="devsite-nav-text" tooltip="">Use DataFrames</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dataframes-data-types" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dataframes-data-types" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dataframes-data-types"><span class="devsite-nav-text" tooltip="">Use the data type system</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dataframes-sessions-io" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dataframes-sessions-io" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dataframes-sessions-io"><span class="devsite-nav-text" tooltip="">Manage sessions and I/O</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dataframes-visualizations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dataframes-visualizations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dataframes-visualizations"><span class="devsite-nav-text" tooltip="">Visualize graphs</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/dataframes-dbt" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dataframes-dbt" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dataframes-dbt"><span class="devsite-nav-text" tooltip="">Use DataFrames in dbt</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use Jupyter notebooks</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/jupyterlab-plugin" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/jupyterlab-plugin" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/jupyterlab-plugin"><span class="devsite-nav-text" tooltip="">Use the BigQuery JupyterLab plugin</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use analysis and BI tools</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/data-analysis-tools-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-analysis-tools-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-analysis-tools-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/connected-sheets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/connected-sheets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/connected-sheets"><span class="devsite-nav-text" tooltip="">Use Connected Sheets</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analyze-data-tableau" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analyze-data-tableau" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analyze-data-tableau"><span class="devsite-nav-text" tooltip="">Use Tableau Desktop</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/looker" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/looker" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/looker"><span class="devsite-nav-text" tooltip="">Use Looker</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/visualize-looker-studio" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/visualize-looker-studio" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/visualize-looker-studio"><span class="devsite-nav-text" tooltip="">Use Looker Studio</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/third-party-integration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/third-party-integration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/third-party-integration"><span class="devsite-nav-text" tooltip="">Use third-party tools</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Google Cloud Ready - BigQuery</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-external"><a href="/bigquery/docs/bigquery-ready-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bigquery-ready-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bigquery-ready-overview"><span class="devsite-nav-text" tooltip="">Overview</span><span class="devsite-nav-icon material-icons" data-icon="external" data-title="External" aria-hidden="true"></span></a></li><li class="devsite-nav-item
           devsite-nav-external"><a href="/bigquery/docs/bigquery-ready-partners" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bigquery-ready-partners" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bigquery-ready-partners"><span class="devsite-nav-text" tooltip="">Partners</span><span class="devsite-nav-icon material-icons" data-icon="external" data-title="External" aria-hidden="true"></span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">AI and machine learning</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/bqml-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bqml-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bqml-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Generative AI and pretrained models</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Choose generative AI and task-specific functions</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/choose-ml-text-function" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/choose-ml-text-function" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/choose-ml-text-function"><span class="devsite-nav-text" tooltip="">Choose a natural language processing function</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/choose-document-processing-function" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/choose-document-processing-function" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/choose-document-processing-function"><span class="devsite-nav-text" tooltip="">Choose a document processing function</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/choose-transcription-function" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/choose-transcription-function" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/choose-transcription-function"><span class="devsite-nav-text" tooltip="">Choose a transcription function</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Generative AI</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/generative-ai-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generative-ai-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generative-ai-overview"><span class="devsite-nav-text" tooltip="">Overview</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Built-in models</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/timesfm-model" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/timesfm-model" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/timesfm-model"><span class="devsite-nav-text" tooltip="">The TimesFM time series forecasting model</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Tutorials</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Generate text</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/generate-text-tutorial-gemini" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-text-tutorial-gemini" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-text-tutorial-gemini"><span class="devsite-nav-text" tooltip="">Generate text using public data and Gemini</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/generate-text-tutorial-gemma" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-text-tutorial-gemma" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-text-tutorial-gemma"><span class="devsite-nav-text" tooltip="">Generate text using public data and Gemma</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/generate-text" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-text" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-text"><span class="devsite-nav-text" tooltip="">Generate text using your data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/iterate-generate-text-calls" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/iterate-generate-text-calls" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/iterate-generate-text-calls"><span class="devsite-nav-text" tooltip="">Handle quota errors by calling ML.GENERATE_TEXT iteratively</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/image-analysis" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/image-analysis" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/image-analysis"><span class="devsite-nav-text" tooltip="">Analyze images with a Gemini vision model</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Tune text generation models</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/generate-text-tuning" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-text-tuning" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-text-tuning"><span class="devsite-nav-text" tooltip="">Tune a model using your data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/tune-evaluate" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/tune-evaluate" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/tune-evaluate"><span class="devsite-nav-text" tooltip="">Use tuning and evaluation to improve model performance</span></a></li></ul></div></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Generate structured data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/generate-table" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-table" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-table"><span class="devsite-nav-text" tooltip="">Generate structured data</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Generate embeddings</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/generate-text-embedding" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-text-embedding" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-text-embedding"><span class="devsite-nav-text" tooltip="">Generate text embeddings using an LLM</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/generate-visual-content-embedding" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-visual-content-embedding" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-visual-content-embedding"><span class="devsite-nav-text" tooltip="">Generate image embeddings using an LLM</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/generate-video-embedding" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-video-embedding" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-video-embedding"><span class="devsite-nav-text" tooltip="">Generate video embeddings using an LLM</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/iterate-generate-embedding-calls" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/iterate-generate-embedding-calls" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/iterate-generate-embedding-calls"><span class="devsite-nav-text" tooltip="">Handle quota errors by calling ML.GENERATE_EMBEDDING iteratively</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/generate-multimodal-embeddings" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-multimodal-embeddings" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-multimodal-embeddings"><span class="devsite-nav-text" tooltip="">Generate and search multimodal embeddings</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/generate-embedding-with-tensorflow-models" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/generate-embedding-with-tensorflow-models" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/generate-embedding-with-tensorflow-models"><span class="devsite-nav-text" tooltip="">Generate text embeddings using pretrained TensorFlow models</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Vector search</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/vector-search" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/vector-search" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/vector-search"><span class="devsite-nav-text" tooltip="">Search embeddings with vector search</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/vector-index-text-search-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/vector-index-text-search-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/vector-index-text-search-tutorial"><span class="devsite-nav-text" tooltip="">Perform semantic search and retrieval-augmented generation</span></a></li></ul></div></li></ul></div></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Task-specific solutions</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/ai-application-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/ai-application-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/ai-application-overview"><span class="devsite-nav-text" tooltip="">Overview</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Tutorials</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Natural language processing</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/understand-text" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/understand-text" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/understand-text"><span class="devsite-nav-text" tooltip="">Understand text</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/translate-text" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/translate-text" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/translate-text"><span class="devsite-nav-text" tooltip="">Translate text</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Document processing</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/process-document" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/process-document" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/process-document"><span class="devsite-nav-text" tooltip="">Process documents</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/rag-pipeline-pdf" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/rag-pipeline-pdf" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/rag-pipeline-pdf"><span class="devsite-nav-text" tooltip="">Parse PDFs in a retrieval-augmented generation pipeline</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Speech recognition</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/transcribe" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/transcribe" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/transcribe"><span class="devsite-nav-text" tooltip="">Transcribe audio files</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Computer vision</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/annotate-image" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/annotate-image" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/annotate-image"><span class="devsite-nav-text" tooltip="">Annotate images</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/object-table-inference" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/object-table-inference" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/object-table-inference"><span class="devsite-nav-text" tooltip="">Run inference on image data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/inference-tutorial-resnet" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/inference-tutorial-resnet" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/inference-tutorial-resnet"><span class="devsite-nav-text" tooltip="">Analyze images with an imported classification model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/inference-tutorial-mobilenet" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/inference-tutorial-mobilenet" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/inference-tutorial-mobilenet"><span class="devsite-nav-text" tooltip="">Analyze images with an imported feature vector model</span></a></li></ul></div></li></ul></div></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Machine learning</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">ML models and MLOps</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/e2e-journey" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/e2e-journey" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/e2e-journey"><span class="devsite-nav-text" tooltip="">End-to-end journey per model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/model-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/model-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/model-overview"><span class="devsite-nav-text" tooltip="">Model creation</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/hp-tuning-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/hp-tuning-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/hp-tuning-overview"><span class="devsite-nav-text" tooltip="">Hyperparameter tuning overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/evaluate-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/evaluate-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/evaluate-overview"><span class="devsite-nav-text" tooltip="">Model evaluation overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/inference-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/inference-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/inference-overview"><span class="devsite-nav-text" tooltip="">Model inference overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/xai-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/xai-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/xai-overview"><span class="devsite-nav-text" tooltip="">Explainable AI overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/weights-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/weights-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/weights-overview"><span class="devsite-nav-text" tooltip="">Model weights overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/ml-pipelines-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/ml-pipelines-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/ml-pipelines-overview"><span class="devsite-nav-text" tooltip="">ML pipelines overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/model-monitoring-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/model-monitoring-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/model-monitoring-overview"><span class="devsite-nav-text" tooltip="">Model monitoring overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/managing-models-vertex" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-models-vertex" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-models-vertex"><span class="devsite-nav-text" tooltip="">Manage BigQueryML models in Vertex AI</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use cases</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/forecasting-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/forecasting-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/forecasting-overview"><span class="devsite-nav-text" tooltip="">Forecasting</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/anomaly-detection-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/anomaly-detection-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/anomaly-detection-overview"><span class="devsite-nav-text" tooltip="">Anomaly detection</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/recommendation-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/recommendation-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/recommendation-overview"><span class="devsite-nav-text" tooltip="">Recommendation</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/classification-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/classification-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/classification-overview"><span class="devsite-nav-text" tooltip="">Classification</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/regression-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/regression-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/regression-overview"><span class="devsite-nav-text" tooltip="">Regression</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dimensionality-reduction-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dimensionality-reduction-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dimensionality-reduction-overview"><span class="devsite-nav-text" tooltip="">Dimensionality reduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/clustering-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/clustering-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/clustering-overview"><span class="devsite-nav-text" tooltip="">Clustering</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Tutorials</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/create-machine-learning-model" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-machine-learning-model" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-machine-learning-model"><span class="devsite-nav-text" tooltip="">Get started with BigQuery ML using SQL</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/create-machine-learning-model-console" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-machine-learning-model-console" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-machine-learning-model-console"><span class="devsite-nav-text" tooltip="">Get started with BigQuery ML using the Cloud console</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Regression and classification</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/linear-regression-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/linear-regression-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/linear-regression-tutorial"><span class="devsite-nav-text" tooltip="">Create a linear regression model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/logistic-regression-prediction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/logistic-regression-prediction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/logistic-regression-prediction"><span class="devsite-nav-text" tooltip="">Create a logistic regression classification model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/boosted-tree-classifier-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/boosted-tree-classifier-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/boosted-tree-classifier-tutorial"><span class="devsite-nav-text" tooltip="">Create a boosted tree classification model</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Clustering</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/kmeans-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/kmeans-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/kmeans-tutorial"><span class="devsite-nav-text" tooltip="">Cluster data with a k-means model</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Recommendation</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/bigqueryml-mf-explicit-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bigqueryml-mf-explicit-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bigqueryml-mf-explicit-tutorial"><span class="devsite-nav-text" tooltip="">Create recommendations based on explicit feedback with a matrix factorization model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/bigqueryml-mf-implicit-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bigqueryml-mf-implicit-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bigqueryml-mf-implicit-tutorial"><span class="devsite-nav-text" tooltip="">Create recommendations based on implicit feedback with a matrix factorization model</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Time series forecasting</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/arima-single-time-series-forecasting-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/arima-single-time-series-forecasting-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/arima-single-time-series-forecasting-tutorial"><span class="devsite-nav-text" tooltip="">Forecast a single time series with an ARIMA_PLUS univariate model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/arima-multiple-time-series-forecasting-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/arima-multiple-time-series-forecasting-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/arima-multiple-time-series-forecasting-tutorial"><span class="devsite-nav-text" tooltip="">Forecast multiple time series with an ARIMA_PLUS univariate model</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/timesfm-time-series-forecasting-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/timesfm-time-series-forecasting-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/timesfm-time-series-forecasting-tutorial"><span class="devsite-nav-text" tooltip="">Forecast time series with a TimesFM univariate model</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/arima-speed-up-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/arima-speed-up-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/arima-speed-up-tutorial"><span class="devsite-nav-text" tooltip="">Scale an ARIMA_PLUS univariate model to millions of time series</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial"><span class="devsite-nav-text" tooltip="">Forecast a single time series with a multivariate model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/arima-plus-xreg-multiple-time-series-forecasting-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/arima-plus-xreg-multiple-time-series-forecasting-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/arima-plus-xreg-multiple-time-series-forecasting-tutorial"><span class="devsite-nav-text" tooltip="">Forecast multiple time series with a multivariate model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/time-series-forecasting-holidays-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/time-series-forecasting-holidays-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/time-series-forecasting-holidays-tutorial"><span class="devsite-nav-text" tooltip="">Use custom holidays with an ARIMA_PLUS univariate model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/arima-time-series-forecasting-with-limits-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/arima-time-series-forecasting-with-limits-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/arima-time-series-forecasting-with-limits-tutorial"><span class="devsite-nav-text" tooltip="">Limit forecasted values for an ARIMA_PLUS univariate model</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series"><span class="devsite-nav-text" tooltip="">Forecast hierarchical time series with an ARIMA_PLUS univariate model</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Anomaly detection</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/time-series-anomaly-detection-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/time-series-anomaly-detection-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/time-series-anomaly-detection-tutorial"><span class="devsite-nav-text" tooltip="">Anomaly detection with a multivariate time series</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Imported and remote models</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/making-predictions-with-imported-tensorflow-models" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/making-predictions-with-imported-tensorflow-models" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/making-predictions-with-imported-tensorflow-models"><span class="devsite-nav-text" tooltip="">Make predictions with imported TensorFlow models</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/making-predictions-with-sklearn-models-in-onnx-format" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/making-predictions-with-sklearn-models-in-onnx-format" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/making-predictions-with-sklearn-models-in-onnx-format"><span class="devsite-nav-text" tooltip="">Make predictions with scikit-learn models in ONNX format</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/making-predictions-with-pytorch-models-in-onnx-format" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/making-predictions-with-pytorch-models-in-onnx-format" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/making-predictions-with-pytorch-models-in-onnx-format"><span class="devsite-nav-text" tooltip="">Make predictions with PyTorch models in ONNX format</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/bigquery-ml-remote-model-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bigquery-ml-remote-model-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bigquery-ml-remote-model-tutorial"><span class="devsite-nav-text" tooltip="">Make predictions with remote models on Vertex AI</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Hyperparameter tuning</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/hyperparameter-tuning-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/hyperparameter-tuning-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/hyperparameter-tuning-tutorial"><span class="devsite-nav-text" tooltip="">Improve model performance with hyperparameter tuning</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Export models</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/export-model-tutorial" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/export-model-tutorial" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/export-model-tutorial"><span class="devsite-nav-text" tooltip="">Export a BigQuery ML model for online prediction</span></a></li></ul></div></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Augmented analytics</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/contribution-analysis" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/contribution-analysis" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/contribution-analysis"><span class="devsite-nav-text" tooltip="">Contribution analysis</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Tutorials</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/get-contribution-analysis-insights" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/get-contribution-analysis-insights" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/get-contribution-analysis-insights"><span class="devsite-nav-text" tooltip="">Get data insights from contribution analysis using a summable metric</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/get-contribution-analysis-insights-sum-ratio" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/get-contribution-analysis-insights-sum-ratio" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/get-contribution-analysis-insights-sum-ratio"><span class="devsite-nav-text" tooltip="">Get data insights from contribution analysis using a summable ratio metric</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Create and manage features</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/preprocess-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/preprocess-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/preprocess-overview"><span class="devsite-nav-text" tooltip="">Feature preprocessing overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/input-feature-types" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/input-feature-types" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/input-feature-types"><span class="devsite-nav-text" tooltip="">Supported input feature types</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/auto-preprocessing" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/auto-preprocessing" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/auto-preprocessing"><span class="devsite-nav-text" tooltip="">Automatic preprocessing</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/manual-preprocessing" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/manual-preprocessing" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/manual-preprocessing"><span class="devsite-nav-text" tooltip="">Manual preprocessing</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/feature-serving" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/feature-serving" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/feature-serving"><span class="devsite-nav-text" tooltip="">Feature serving</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/bigqueryml-transform" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bigqueryml-transform" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bigqueryml-transform"><span class="devsite-nav-text" tooltip="">Perform feature engineering with the TRANSFORM clause</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Work with models</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/listing-models" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/listing-models" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/listing-models"><span class="devsite-nav-text" tooltip="">List models</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/managing-models" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-models" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-models"><span class="devsite-nav-text" tooltip="">Manage models</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/getting-model-metadata" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/getting-model-metadata" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/getting-model-metadata"><span class="devsite-nav-text" tooltip="">Get model metadata</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/updating-model-metadata" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/updating-model-metadata" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/updating-model-metadata"><span class="devsite-nav-text" tooltip="">Update model metadata</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/exporting-models" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/exporting-models" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/exporting-models"><span class="devsite-nav-text" tooltip="">Export models</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/deleting-models" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/deleting-models" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/deleting-models"><span class="devsite-nav-text" tooltip="">Delete models</span></a></li></ul></div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/reference-patterns" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reference-patterns" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reference-patterns"><span class="devsite-nav-text" tooltip="">Reference patterns</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Administer</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/admin-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/admin-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/admin-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage resources</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/resource-hierarchy" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/resource-hierarchy" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/resource-hierarchy"><span class="devsite-nav-text" tooltip="">Organize resources</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reliability-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reliability-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reliability-intro"><span class="devsite-nav-text" tooltip="">Understand reliability</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage code assets</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/manage-data-preparations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/manage-data-preparations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/manage-data-preparations"><span class="devsite-nav-text" tooltip="">Manage data preparations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/manage-notebooks" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/manage-notebooks" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/manage-notebooks"><span class="devsite-nav-text" tooltip="">Manage notebooks</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/manage-saved-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/manage-saved-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/manage-saved-queries"><span class="devsite-nav-text" tooltip="">Manage saved queries</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/manage-pipelines" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/manage-pipelines" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/manage-pipelines"><span class="devsite-nav-text" tooltip="">Manage pipelines</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage tables</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/managing-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-tables"><span class="devsite-nav-text" tooltip="">Manage tables</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/managing-table-data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-table-data" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-table-data"><span class="devsite-nav-text" tooltip="">Manage table data</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/managing-table-schemas" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-table-schemas" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-table-schemas"><span class="devsite-nav-text" tooltip="">Modify table schemas</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/restore-deleted-tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/restore-deleted-tables" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/restore-deleted-tables"><span class="devsite-nav-text" tooltip="">Restore deleted tables</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage table clones</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/table-clones-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-clones-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-clones-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-clones-create" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-clones-create" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-clones-create"><span class="devsite-nav-text" tooltip="">Create table clones</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage table snapshots</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/table-snapshots-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-snapshots-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-snapshots-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-snapshots-create" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-snapshots-create" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-snapshots-create"><span class="devsite-nav-text" tooltip="">Create table snapshots</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-snapshots-restore" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-snapshots-restore" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-snapshots-restore"><span class="devsite-nav-text" tooltip="">Restore table snapshots</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-snapshots-list" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-snapshots-list" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-snapshots-list"><span class="devsite-nav-text" tooltip="">List table snapshots</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-snapshots-metadata" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-snapshots-metadata" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-snapshots-metadata"><span class="devsite-nav-text" tooltip="">View table snapshot metadata</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-snapshots-update" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-snapshots-update" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-snapshots-update"><span class="devsite-nav-text" tooltip="">Update table snapshot metadata</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-snapshots-delete" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-snapshots-delete" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-snapshots-delete"><span class="devsite-nav-text" tooltip="">Delete table snapshots</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/table-snapshots-scheduled" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/table-snapshots-scheduled" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/table-snapshots-scheduled"><span class="devsite-nav-text" tooltip="">Create periodic table snapshots</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/default-configuration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/default-configuration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/default-configuration"><span class="devsite-nav-text" tooltip="">Manage configuration settings</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage datasets</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/managing-datasets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-datasets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-datasets"><span class="devsite-nav-text" tooltip="">Manage datasets</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/updating-datasets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/updating-datasets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/updating-datasets"><span class="devsite-nav-text" tooltip="">Update dataset properties</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/restore-deleted-datasets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/restore-deleted-datasets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/restore-deleted-datasets"><span class="devsite-nav-text" tooltip="">Restore deleted datasets</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/materialized-views-manage" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/materialized-views-manage" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/materialized-views-manage"><span class="devsite-nav-text" tooltip="">Manage materialized views</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/materialized-view-replicas-manage" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/materialized-view-replicas-manage" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/materialized-view-replicas-manage"><span class="devsite-nav-text" tooltip="">Manage materialized view replicas</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Schedule resources</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/orchestrate-workloads" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/orchestrate-workloads" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/orchestrate-workloads"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Schedule code assets</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/orchestrate-data-preparations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/orchestrate-data-preparations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/orchestrate-data-preparations"><span class="devsite-nav-text" tooltip="">Schedule data preparations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/orchestrate-notebooks" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/orchestrate-notebooks" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/orchestrate-notebooks"><span class="devsite-nav-text" tooltip="">Schedule notebooks</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/schedule-pipelines" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/schedule-pipelines" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/schedule-pipelines"><span class="devsite-nav-text" tooltip="">Schedule pipelines</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/orchestrate-dags" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/orchestrate-dags" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/orchestrate-dags"><span class="devsite-nav-text" tooltip="">Schedule DAGs</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Schedule jobs and queries</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/running-jobs" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/running-jobs" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/running-jobs"><span class="devsite-nav-text" tooltip="">Run jobs programmatically</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/scheduling-queries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/scheduling-queries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/scheduling-queries"><span class="devsite-nav-text" tooltip="">Schedule queries</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Workload management</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/slots" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/slots" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/slots"><span class="devsite-nav-text" tooltip="">Slots</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-workload-management" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-workload-management" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-workload-management"><span class="devsite-nav-text" tooltip="">Slot reservations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/slots-autoscaling-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/slots-autoscaling-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/slots-autoscaling-intro"><span class="devsite-nav-text" tooltip="">Slots autoscaling</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Use reservations</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-get-started" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-get-started" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-get-started"><span class="devsite-nav-text" tooltip="">Get started</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/slot-estimator" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/slot-estimator" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/slot-estimator"><span class="devsite-nav-text" tooltip="">Estimate slot capacity requirements</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/slot-recommender" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/slot-recommender" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/slot-recommender"><span class="devsite-nav-text" tooltip="">View slot recommendations and insights</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-commitments" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-commitments" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-commitments"><span class="devsite-nav-text" tooltip="">Purchase and manage slot commitments</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-tasks" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-tasks" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-tasks"><span class="devsite-nav-text" tooltip="">Work with slot reservations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-assignments" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-assignments" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-assignments"><span class="devsite-nav-text" tooltip="">Work with reservation assignments</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/managing-jobs" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-jobs" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-jobs"><span class="devsite-nav-text" tooltip="">Manage jobs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/query-queues" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/query-queues" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/query-queues"><span class="devsite-nav-text" tooltip="">Use query queues</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Legacy reservations</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-intro-legacy" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-intro-legacy" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-intro-legacy"><span class="devsite-nav-text" tooltip="">Introduction to legacy reservations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-details-legacy" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-details-legacy" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-details-legacy"><span class="devsite-nav-text" tooltip="">Legacy slot commitments</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-commitments-legacy" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-commitments-legacy" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-commitments-legacy"><span class="devsite-nav-text" tooltip="">Purchase and manage legacy slot commitments</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-tasks-legacy" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-tasks-legacy" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-tasks-legacy"><span class="devsite-nav-text" tooltip="">Work with legacy slot reservations</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage BI Engine</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/bi-engine-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bi-engine-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bi-engine-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/bi-engine-reserve-capacity" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bi-engine-reserve-capacity" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bi-engine-reserve-capacity"><span class="devsite-nav-text" tooltip="">Reserve BI Engine capacity</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Monitor workloads</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/monitoring" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/monitoring" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/monitoring"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/admin-resource-charts" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/admin-resource-charts" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/admin-resource-charts"><span class="devsite-nav-text" tooltip="">Monitor resource utilization</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/admin-jobs-explorer" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/admin-jobs-explorer" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/admin-jobs-explorer"><span class="devsite-nav-text" tooltip="">Monitor jobs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-monitor-listings" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-monitor-listings" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-monitor-listings"><span class="devsite-nav-text" tooltip="">Monitor sharing listings</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/bi-engine-monitor" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/bi-engine-monitor" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/bi-engine-monitor"><span class="devsite-nav-text" tooltip="">Monitor BI Engine</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dts-monitor" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dts-monitor" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dts-monitor"><span class="devsite-nav-text" tooltip="">Monitor Data Transfer Service</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/materialized-views-monitor" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/materialized-views-monitor" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/materialized-views-monitor"><span class="devsite-nav-text" tooltip="">Monitor materialized views</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reservations-monitoring" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reservations-monitoring" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reservations-monitoring"><span class="devsite-nav-text" tooltip="">Monitor reservations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/continuous-queries-monitor" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/continuous-queries-monitor" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/continuous-queries-monitor"><span class="devsite-nav-text" tooltip="">Monitor continuous queries</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/monitoring-dashboard" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/monitoring-dashboard" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/monitoring-dashboard"><span class="devsite-nav-text" tooltip="">Dashboards, charts, and alerts</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/create-alert-scheduled-query" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-alert-scheduled-query" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-alert-scheduled-query"><span class="devsite-nav-text" tooltip="">Set up alerts with scheduled queries</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Optimize resources</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Control costs</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-costs" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-costs" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-costs"><span class="devsite-nav-text" tooltip="">Estimate and control costs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/custom-quotas" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/custom-quotas" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/custom-quotas"><span class="devsite-nav-text" tooltip="">Create custom query quotas</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Optimize with recommendations</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/recommendations-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/recommendations-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/recommendations-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/manage-partition-cluster-recommendations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/manage-partition-cluster-recommendations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/manage-partition-cluster-recommendations"><span class="devsite-nav-text" tooltip="">Manage cluster and partition recommendations</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/manage-materialized-recommendations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/manage-materialized-recommendations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/manage-materialized-recommendations"><span class="devsite-nav-text" tooltip="">Manage materialized view recommendations</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Organize with labels</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/labels-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/labels-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/labels-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/adding-labels" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/adding-labels" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/adding-labels"><span class="devsite-nav-text" tooltip="">Add labels</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/viewing-labels" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/viewing-labels" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/viewing-labels"><span class="devsite-nav-text" tooltip="">View labels</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/updating-labels" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/updating-labels" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/updating-labels"><span class="devsite-nav-text" tooltip="">Update labels</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/filtering-labels" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/filtering-labels" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/filtering-labels"><span class="devsite-nav-text" tooltip="">Filter using labels</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/deleting-labels" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/deleting-labels" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/deleting-labels"><span class="devsite-nav-text" tooltip="">Delete labels</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Govern</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/data-governance" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-governance" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-governance"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage data quality</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/data-quality-scan" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-quality-scan" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-quality-scan"><span class="devsite-nav-text" tooltip="">Scan for data quality issues</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-catalog-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-catalog-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-catalog-overview"><span class="devsite-nav-text" tooltip="">Data Catalog overview</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-catalog" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-catalog" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-catalog"><span class="devsite-nav-text" tooltip="">Work with Data Catalog</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Control access to resources</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/access-control-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/access-control-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/access-control-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/access-control" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/access-control" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/access-control"><span class="devsite-nav-text" tooltip="">IAM roles and permissions</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/dataset-access-control" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/dataset-access-control" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/dataset-access-control"><span class="devsite-nav-text" tooltip="">Changes to dataset-level access controls</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/access-control-basic-roles" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/access-control-basic-roles" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/access-control-basic-roles"><span class="devsite-nav-text" tooltip="">Basic roles and permissions</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Control access with IAM</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/control-access-to-resources-iam" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/control-access-to-resources-iam" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/control-access-to-resources-iam"><span class="devsite-nav-text" tooltip="">Control access to resources with IAM</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/tags" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/tags" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/tags"><span class="devsite-nav-text" tooltip="">Control access with tags</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/conditions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/conditions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/conditions"><span class="devsite-nav-text" tooltip="">Control access with conditions</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/custom-constraints" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/custom-constraints" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/custom-constraints"><span class="devsite-nav-text" tooltip="">Control access with custom constraints</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Control access with authorization</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/authorized-datasets" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/authorized-datasets" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/authorized-datasets"><span class="devsite-nav-text" tooltip="">Authorized datasets</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/authorized-routines" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/authorized-routines" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/authorized-routines"><span class="devsite-nav-text" tooltip="">Authorized routines</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/authorized-views" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/authorized-views" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/authorized-views"><span class="devsite-nav-text" tooltip="">Authorized views</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Tutorials</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/create-authorized-views" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/create-authorized-views" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/create-authorized-views"><span class="devsite-nav-text" tooltip="">Create an authorized view</span></a></li></ul></div></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Restrict network access</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/vpc-sc" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/vpc-sc" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/vpc-sc"><span class="devsite-nav-text" tooltip="">Control access with VPC service controls</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/regional-endpoints" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/regional-endpoints" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/regional-endpoints"><span class="devsite-nav-text" tooltip="">Regional endpoints</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Control column and row access</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Control access to table columns</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/column-level-security-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/column-level-security-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/column-level-security-intro"><span class="devsite-nav-text" tooltip="">Introduction to column-level access control</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/column-level-security" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/column-level-security" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/column-level-security"><span class="devsite-nav-text" tooltip="">Restrict access with column-level access control</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/column-level-security-writes" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/column-level-security-writes" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/column-level-security-writes"><span class="devsite-nav-text" tooltip="">Impact on writes</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Control access to table rows</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/row-level-security-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/row-level-security-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/row-level-security-intro"><span class="devsite-nav-text" tooltip="">Introduction to row-level security</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/managing-row-level-security" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-row-level-security" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-row-level-security"><span class="devsite-nav-text" tooltip="">Work with row-level security</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/using-row-level-security-with-features" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/using-row-level-security-with-features" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/using-row-level-security-with-features"><span class="devsite-nav-text" tooltip="">Use row-level security with other BigQuery features</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-row-level-security" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-row-level-security" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-row-level-security"><span class="devsite-nav-text" tooltip="">Best practices for row-level security</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage policy tags</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/managing-policy-tags-across-locations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/managing-policy-tags-across-locations" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/managing-policy-tags-across-locations"><span class="devsite-nav-text" tooltip="">Manage policy tags across locations</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/best-practices-policy-tags" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/best-practices-policy-tags" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/best-practices-policy-tags"><span class="devsite-nav-text" tooltip="">Best practices for using policy tags</span></a></li></ul></div></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Protect sensitive data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Mask data in table columns</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/column-data-masking-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/column-data-masking-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/column-data-masking-intro"><span class="devsite-nav-text" tooltip="">Introduction to data masking</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/column-data-masking" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/column-data-masking" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/column-data-masking"><span class="devsite-nav-text" tooltip="">Mask column data</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Anonymize data with differential privacy</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/differential-privacy" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/differential-privacy" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/differential-privacy"><span class="devsite-nav-text" tooltip="">Use differential privacy</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/extend-differential-privacy" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/extend-differential-privacy" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/extend-differential-privacy"><span class="devsite-nav-text" tooltip="">Extend differential privacy</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/analysis-rules" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analysis-rules" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analysis-rules"><span class="devsite-nav-text" tooltip="">Restrict data access using analysis rules</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/scan-with-dlp" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/scan-with-dlp" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/scan-with-dlp"><span class="devsite-nav-text" tooltip="">Use Sensitive Data Protection</span></a></li></ul></div></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Manage encryption</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/encryption-at-rest" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/encryption-at-rest" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/encryption-at-rest"><span class="devsite-nav-text" tooltip="">Encryption at rest</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/customer-managed-encryption" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/customer-managed-encryption" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/customer-managed-encryption"><span class="devsite-nav-text" tooltip="">Customer-managed encryption keys</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/column-key-encrypt" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/column-key-encrypt" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/column-key-encrypt"><span class="devsite-nav-text" tooltip="">Column-level encryption with Cloud KMS</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/aead-encryption-concepts" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/aead-encryption-concepts" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/aead-encryption-concepts"><span class="devsite-nav-text" tooltip="">AEAD encryption</span></a></li></ul></div></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Share data</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-introduction" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-introduction" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-introduction"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-manage-exchanges" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-manage-exchanges" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-manage-exchanges"><span class="devsite-nav-text" tooltip="">Manage data exchanges</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-manage-listings" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-manage-listings" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-manage-listings"><span class="devsite-nav-text" tooltip="">Manage listings</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-manage-subscriptions" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-manage-subscriptions" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-manage-subscriptions"><span class="devsite-nav-text" tooltip="">Manage subscriptions</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-grant-roles" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-grant-roles" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-grant-roles"><span class="devsite-nav-text" tooltip="">Configure user roles</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-view-subscribe-listings" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-view-subscribe-listings" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-view-subscribe-listings"><span class="devsite-nav-text" tooltip="">View and subscribe to listings</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/data-clean-rooms" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/data-clean-rooms" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/data-clean-rooms"><span class="devsite-nav-text" tooltip="">Share sensitive data with data clean rooms</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Entity resolution</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/entity-resolution-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/entity-resolution-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/entity-resolution-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/entity-resolution-setup" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/entity-resolution-setup" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/entity-resolution-setup"><span class="devsite-nav-text" tooltip="">Use entity resolution</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-vpc-sc-rules" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-vpc-sc-rules" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-vpc-sc-rules"><span class="devsite-nav-text" tooltip="">VPC Service Controls for Sharing</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-stream-sharing" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-stream-sharing" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-stream-sharing"><span class="devsite-nav-text" tooltip="">Stream sharing with Pub/Sub</span></a></li><li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/analytics-hub-cloud-marketplace" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-cloud-marketplace" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-cloud-marketplace"><span class="devsite-nav-text" tooltip="">Commercialize listings on Cloud Marketplace</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Audit</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/introduction-audit-workloads" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/introduction-audit-workloads" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/introduction-audit-workloads"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/auditing-policy-tags" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/auditing-policy-tags" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/auditing-policy-tags"><span class="devsite-nav-text" tooltip="">Audit policy tags</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/column-data-masking-audit-logging" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/column-data-masking-audit-logging" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/column-data-masking-audit-logging"><span class="devsite-nav-text" tooltip="">View Data Policy audit logs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/audit-logging" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/audit-logging" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/audit-logging"><span class="devsite-nav-text" tooltip="">Data Transfer Service audit logs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/analytics-hub-audit-logging" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/analytics-hub-audit-logging" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/analytics-hub-audit-logging"><span class="devsite-nav-text" tooltip="">Sharing audit logs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reference/auditlogs" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reference/auditlogs" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reference/auditlogs"><span class="devsite-nav-text" tooltip="">BigQuery audit logs reference</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reference/auditlogs/migration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reference/auditlogs/migration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reference/auditlogs/migration"><span class="devsite-nav-text" tooltip="">Migrate audit logs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/biglake-audit-logging" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/biglake-audit-logging" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/biglake-audit-logging"><span class="devsite-nav-text" tooltip="">BigLake API audit logs</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/reference/auditlogs/audit-logging-bq-migration" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reference/auditlogs/audit-logging-bq-migration" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reference/auditlogs/audit-logging-bq-migration"><span class="devsite-nav-text" tooltip="">BigQuery Migration API audit logs</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-heading"><div class="devsite-nav-title devsite-nav-title-no-path">
        <span class="devsite-nav-text" tooltip="">Develop</span>
      </div></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/developer-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/developer-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/developer-overview"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/samples" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/samples" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/samples"><span class="devsite-nav-text" tooltip="">BigQuery code samples</span></a></li>

  <li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">BigQuery API basics</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/reference/libraries-overview" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reference/libraries-overview" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reference/libraries-overview"><span class="devsite-nav-text" tooltip="">BigQuery APIs and libraries overview</span></a></li><li class="devsite-nav-item
           devsite-nav-expandable"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Authentication</span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/authentication" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/authentication" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/authentication"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/authentication/getting-started" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/authentication/getting-started" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/authentication/getting-started"><span class="devsite-nav-text" tooltip="">Get started</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/authentication/end-user-installed" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/authentication/end-user-installed" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/authentication/end-user-installed"><span class="devsite-nav-text" tooltip="">Authenticate as an end user</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/json-web-tokens" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/json-web-tokens" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/json-web-tokens"><span class="devsite-nav-text" tooltip="">Authenticate with JSON Web Tokens</span></a></li></ul></div></li><li class="devsite-nav-item"><a href="/bigquery/docs/running-jobs" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/running-jobs" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/running-jobs"><span class="devsite-nav-text" tooltip="">Run jobs programmatically</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/paging-results" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/paging-results" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/paging-results"><span class="devsite-nav-text" tooltip="">Paginate with BigQuery API</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/api-performance" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/api-performance" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/api-performance"><span class="devsite-nav-text" tooltip="">API performance tips</span></a></li><li class="devsite-nav-item
           devsite-nav-deprecated"><a href="/bigquery/batch" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/batch" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/batch"><span class="devsite-nav-text" tooltip="">Batch requests</span><span class="devsite-nav-icon material-icons" data-icon="deprecated" data-title="Deprecated" aria-hidden="true"></span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Repositories</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/repository-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/repository-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/repository-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/repositories" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/repositories" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/repositories"><span class="devsite-nav-text" tooltip="">Create repositories</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-expandable
           devsite-nav-preview"><div class="devsite-expandable-nav">
      <a class="devsite-nav-toggle" aria-hidden="true"></a><div class="devsite-nav-title devsite-nav-title-no-path" tabindex="0" role="button">
        <span class="devsite-nav-text" tooltip="">Workspaces</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span>
      </div><ul class="devsite-nav-section"><li class="devsite-nav-item"><a href="/bigquery/docs/workspaces-intro" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/workspaces-intro" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/workspaces-intro"><span class="devsite-nav-text" tooltip="">Introduction</span></a></li><li class="devsite-nav-item"><a href="/bigquery/docs/workspaces" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/workspaces" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/workspaces"><span class="devsite-nav-text" tooltip="">Create and use workspaces</span></a></li></ul></div></li>

  <li class="devsite-nav-item
           devsite-nav-preview"><a href="/bigquery/docs/vs-code-extension" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/vs-code-extension" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/vs-code-extension"><span class="devsite-nav-text" tooltip="">Use the VS Code extension</span><span class="devsite-nav-icon material-icons" data-icon="preview" data-title="Preview" aria-hidden="true"></span></a></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/python-libraries" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/python-libraries" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/python-libraries"><span class="devsite-nav-text" tooltip="">Choose a Python library</span></a></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/reference/odbc-jdbc-drivers" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/reference/odbc-jdbc-drivers" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/reference/odbc-jdbc-drivers"><span class="devsite-nav-text" tooltip="">Use ODBC and JDBC drivers</span></a></li>

  <li class="devsite-nav-item"><a href="/bigquery/docs/pre-built-tools-with-mcp-toolbox" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Book nav link, pathname: /bigquery/docs/pre-built-tools-with-mcp-toolbox" track-type="bookNav" track-name="click" track-metadata-eventdetail="/bigquery/docs/pre-built-tools-with-mcp-toolbox"><span class="devsite-nav-text" tooltip="">Connect your IDE to BigQuery</span></a></li>
          </ul>
        
        
          
    
  
    
      
      <ul class="devsite-nav-list" menu="Technology areas" aria-label="Side menu" hidden="">
        
          
            
            
              
<li class="devsite-nav-item">

  
  <a href="/docs/ai-ml" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: AI and ML" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      AI and ML
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/application-development" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Application development" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Application development
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/application-hosting" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Application hosting" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Application hosting
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/compute-area" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Compute" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Compute
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/data" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Data analytics and pipelines" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Data analytics and pipelines
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/databases" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Databases" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Databases
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/dhm-cloud" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Distributed, hybrid, and multicloud" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Distributed, hybrid, and multicloud
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/generative-ai" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Generative AI" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Generative AI
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/industry" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Industry solutions" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Industry solutions
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/networking" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Networking" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Networking
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/observability" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Observability and monitoring" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Observability and monitoring
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/security" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Security" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Security
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/storage" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Storage" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Storage
   </span>
    
  
  </a>
  

</li>

            
          
        
      </ul>
    
  
    
      
      <ul class="devsite-nav-list" menu="Cross-product tools" aria-label="Side menu" hidden="">
        
          
            
            
              
<li class="devsite-nav-item">

  
  <a href="/docs/access-resources" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Access and resources management" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Access and resources management
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/costs-usage" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Costs and usage management" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Costs and usage management
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/devtools" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud SDK, languages, frameworks, and tools" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud SDK, languages, frameworks, and tools
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/iac" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Infrastructure as code" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Infrastructure as code
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/docs/migration" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Migration" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Migration
   </span>
    
  
  </a>
  

</li>

            
          
        
      </ul>
    
  
    
      
      <ul class="devsite-nav-list" menu="Related sites" aria-label="Side menu" hidden="">
        
          
            
            
              
<li class="devsite-nav-item">

  
  <a href="/" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud Home" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud Home
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/free" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Free Trial and Free Tier" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Free Trial and Free Tier
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/architecture" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Architecture Center" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Architecture Center
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="https://cloud.google.com/blog" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Blog" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Blog
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/contact" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Contact Sales" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Contact Sales
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/developers" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud Developer Center" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud Developer Center
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="https://developers.google.com/" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Developer Center" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Developer Center
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="https://console.cloud.google.com/marketplace" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud Marketplace" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud Marketplace
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/marketplace/docs" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud Marketplace Documentation" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud Marketplace Documentation
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="https://www.cloudskillsboost.google/paths" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud Skills Boost" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud Skills Boost
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/solutions" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud Solution Center" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud Solution Center
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="/support-hub" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud Support" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud Support
   </span>
    
  
  </a>
  

</li>

            
              
<li class="devsite-nav-item">

  
  <a href="https://www.youtube.com/@googlecloudtech" class="devsite-nav-title gc-analytics-event
              
              " data-category="Site-Wide Custom Events" data-label="Responsive Tab: Google Cloud Tech Youtube Channel" track-type="navMenu" track-metadata-eventdetail="globalMenu" track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip="">
      Google Cloud Tech Youtube Channel
   </span>
    
  
  </a>
  

</li>

            
          
        
      </ul>
    
  
        
        
          
    
  
    
  
    
  
    
  
        
      </div>
    
  </div>
</nav>
        
      </devsite-book-nav><div class="devsite-book-nav-blur" fixed="" style="--devsite-js-book-nav-scrollbar-width: 8px;"></div><button class="devsite-book-nav-toggle" aria-haspopup="menu" fixed="" aria-label="Hide side navigation" data-title="Hide side navigation" aria-expanded="true"><span class="material-icons devsite-book-nav-toggle-icon"></span></button>
      <section id="gc-wrapper" style="margin-top: 112.8px;">
        <main role="main" id="main-content" class="devsite-main-content" has-book-nav="" has-sidebar="">
          <div class="devsite-sidebar" fixed="" style="--devsite-js-sidebar-max-height: 534.1999969482422px; --devsite-js-sidebar-offset: 0; --devsite-js-sidebar-max-width: 251.8000030517578px;">
            <div class="devsite-sidebar-content">
                
                <devsite-toc class="devsite-nav devsite-toc" role="navigation" aria-label="On this page" depth="2" scrollbars="" visible=""><ul class="devsite-nav-list"><li class="devsite-nav-item devsite-nav-heading devsite-toc-toggle"><span class="devsite-nav-title" role="heading" aria-level="2"><span class="devsite-nav-text">On this page</span></span></li><li class="devsite-nav-item"><a href="#when_to_use_partitioning" class="devsite-nav-title gc-analytics-event devsite-nav-active" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="0" track-type="navigation" track-name="rightNav" track-metadata-position="0" track-metadata-link-destination="#when_to_use_partitioning"><span class="devsite-nav-text" tooltip="">When to use partitioning</span></a></li><li class="devsite-nav-item"><a href="#types_of_partitioning" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="1" track-type="navigation" track-name="rightNav" track-metadata-position="1" track-metadata-link-destination="#types_of_partitioning"><span class="devsite-nav-text" tooltip="">Types of partitioning</span></a><ul class="devsite-nav-list"><li class="devsite-nav-item"><a href="#integer_range" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="1.0" track-type="navigation" track-name="rightNav" track-metadata-position="1.0" track-metadata-link-destination="#integer_range"><span class="devsite-nav-text" tooltip="">Integer range partitioning</span></a></li><li class="devsite-nav-item"><a href="#date_timestamp_partitioned_tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="1.1" track-type="navigation" track-name="rightNav" track-metadata-position="1.1" track-metadata-link-destination="#date_timestamp_partitioned_tables"><span class="devsite-nav-text" tooltip="">Time-unit column partitioning</span></a></li><li class="devsite-nav-item"><a href="#ingestion_time" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="1.2" track-type="navigation" track-name="rightNav" track-metadata-position="1.2" track-metadata-link-destination="#ingestion_time"><span class="devsite-nav-text" tooltip="">Ingestion time partitioning</span></a></li><li class="devsite-nav-item"><a href="#select_daily_hourly_monthly_or_yearly_partitioning" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="1.3" track-type="navigation" track-name="rightNav" track-metadata-position="1.3" track-metadata-link-destination="#select_daily_hourly_monthly_or_yearly_partitioning"><span class="devsite-nav-text" tooltip="">Select daily, hourly, monthly, or yearly partitioning</span></a></li></ul></li><li class="devsite-nav-item"><a href="#combining_clustered_and_partitioned_tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="2" track-type="navigation" track-name="rightNav" track-metadata-position="2" track-metadata-link-destination="#combining_clustered_and_partitioned_tables"><span class="devsite-nav-text" tooltip="">Combining clustered and partitioned tables</span></a></li><li class="devsite-nav-item"><a href="#dt_partition_shard" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="3" track-type="navigation" track-name="rightNav" track-metadata-position="3" track-metadata-link-destination="#dt_partition_shard"><span class="devsite-nav-text" tooltip="">Partitioning versus sharding</span></a></li><li class="devsite-nav-item"><a href="#partition_decorators" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="4" track-type="navigation" track-name="rightNav" track-metadata-position="4" track-metadata-link-destination="#partition_decorators"><span class="devsite-nav-text" tooltip="">Partition decorators</span></a></li><li class="devsite-nav-item"><a href="#browse-table" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="5" track-type="navigation" track-name="rightNav" track-metadata-position="5" track-metadata-link-destination="#browse-table"><span class="devsite-nav-text" tooltip="">Browse the data in a partition</span></a></li><li class="devsite-nav-item"><a href="#export_table_data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="6" track-type="navigation" track-name="rightNav" track-metadata-position="6" track-metadata-link-destination="#export_table_data"><span class="devsite-nav-text" tooltip="">Export table data</span></a></li><li class="devsite-nav-item"><a href="#limitations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="7" track-type="navigation" track-name="rightNav" track-metadata-position="7" track-metadata-link-destination="#limitations"><span class="devsite-nav-text" tooltip="">Limitations</span></a></li><li class="devsite-nav-item"><a href="#quotas_limits" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="8" track-type="navigation" track-name="rightNav" track-metadata-position="8" track-metadata-link-destination="#quotas_limits"><span class="devsite-nav-text" tooltip="">Quotas and limits</span></a></li><li class="devsite-nav-item"><a href="#pricing" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="9" track-type="navigation" track-name="rightNav" track-metadata-position="9" track-metadata-link-destination="#pricing"><span class="devsite-nav-text" tooltip="">Table pricing</span></a></li><li class="devsite-nav-item"><a href="#table_security" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="10" track-type="navigation" track-name="rightNav" track-metadata-position="10" track-metadata-link-destination="#table_security"><span class="devsite-nav-text" tooltip="">Table security</span></a></li><li class="devsite-nav-item"><a href="#whats_next" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Right nav" data-value="11" track-type="navigation" track-name="rightNav" track-metadata-position="11" track-metadata-link-destination="#whats_next"><span class="devsite-nav-text" tooltip="">What's next</span></a></li></ul></devsite-toc>
                <devsite-recommendations-sidebar class="nocontent devsite-nav">
                </devsite-recommendations-sidebar>
            </div>
          </div>
          <devsite-content>
            
              












<article class="devsite-article">
  
  
  
  
  

  <div class="devsite-article-meta nocontent" role="navigation">
    
    
    <ul class="devsite-breadcrumb-list" aria-label="Breadcrumb">
  
  <li class="devsite-breadcrumb-item
             ">
    
    
    
      
  <a href="https://cloud.google.com/" class="devsite-breadcrumb-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Breadcrumbs" data-value="1" track-type="globalNav" track-name="breadcrumb" track-metadata-position="1" track-metadata-eventdetail="Google Cloud">
    
        Home
      
  </a>
  
    
  </li>
  
  <li class="devsite-breadcrumb-item
             ">
    
      
      <div class="devsite-breadcrumb-guillemet material-icons" aria-hidden="true"></div>
    
    
    
      
  <a href="https://cloud.google.com/bigquery" class="devsite-breadcrumb-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Breadcrumbs" data-value="2" track-type="globalNav" track-name="breadcrumb" track-metadata-position="2" track-metadata-eventdetail="BigQuery: Cloud Data Warehouse">
    
        BigQuery
      
  </a>
  
    
  </li>
  
  <li class="devsite-breadcrumb-item
             ">
    
      
      <div class="devsite-breadcrumb-guillemet material-icons" aria-hidden="true"></div>
    
    
    
      
  <a href="https://cloud.google.com/bigquery/docs" class="devsite-breadcrumb-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Breadcrumbs" data-value="3" track-type="globalNav" track-name="breadcrumb" track-metadata-position="3" track-metadata-eventdetail="BigQuery">
    
        Documentation
      
  </a>
  
    
  </li>
  
  <li class="devsite-breadcrumb-item
             ">
    
      
      <div class="devsite-breadcrumb-guillemet material-icons" aria-hidden="true"></div>
    
    
    
      
  <a href="https://cloud.google.com/bigquery/docs/introduction" class="devsite-breadcrumb-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Breadcrumbs" data-value="4" track-type="globalNav" track-name="breadcrumb" track-metadata-position="4" track-metadata-eventdetail="">
    
        Guides
      
  </a>
  
    
  </li>
  
</ul>
    
      
    <devsite-thumb-rating position="header"><div class="devsite-thumb-rating" role="form" aria-labelledby="devsite-thumb-label-header"><div class="devsite-thumb-label" id="devsite-thumb-label-header">Was this helpful?</div><div class="devsite-thumbs"><button class="devsite-thumb devsite-thumb-up" data-title="Helpful" aria-label="Helpful"><svg class="devsite-thumb-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21,7h-6.31l0.95-4.57l0.03-0.32c0-0.41-0.17-0.79-0.44-1.06L14.17,0c0,0-7.09,6.85-7.17,7H2v13h16 c0.83,0,1.54-0.5,1.84-1.22l3.02-7.05C22.95,11.5,23,11.26,23,11V9C23,7.9,22.1,7,21,7z M7,18H4V9h3V18z M21,11l-3,7H9V8l4.34-4.34 L12,9h9V11z"></path></svg></button><button class="devsite-thumb devsite-thumb-down" data-title="Not helpful" aria-label="Not helpful"><svg class="devsite-thumb-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3,17h6.31l-0.95,4.57l-0.03,0.32c0,0.41,0.17,0.79,0.44,1.06L9.83,24c0,0,7.09-6.85,7.17-7h5V4H6 C5.17,4,4.46,4.5,4.16,5.22l-3.02,7.05C1.05,12.5,1,12.74,1,13v2C1,16.1,1.9,17,3,17z M17,6h3v9h-3V6z M3,13l3-7h9v10l-4.34,4.34 L12,15H3V13z"></path></svg></button></div></div></devsite-thumb-rating>
  
    
  </div>
  
    <devsite-feedback position="header" project-name="BigQuery" product-id="81912" bucket="docs" context="" version="t-devsite-webserver-20250805-r00-rc04.471103249751607376" data-label="Send Feedback Button" track-type="feedback" track-name="sendFeedbackLink" track-metadata-position="header" class="nocontent" project-feedback-url="https://issuetracker.google.com/issues/new?component=187149&amp;template=0" project-icon="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/favicons/onecloud/super_cloud.png" project-support-url="https://cloud.google.com/bigquery/docs/getting-support">

  <button>
  
    
    Send feedback
  
  </button>
</devsite-feedback>
  
  
    
  

  <devsite-toc class="devsite-nav devsite-toc-embedded" depth="2" devsite-toc-embedded="" expandable="" visible=""><ul class="devsite-nav-list"><li class="devsite-nav-item devsite-nav-heading devsite-toc-toggle"><span class="devsite-nav-title" role="heading" aria-level="2"><span class="devsite-nav-text">On this page</span></span><button type="button" title="Expand/collapse contents" class="devsite-nav-show-all button-transparent material-icons"></button></li><li class="devsite-nav-item" visible=""><a href="#when_to_use_partitioning" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="0" track-type="navigation" track-name="embeddedNav" track-metadata-position="0" track-metadata-link-destination="#when_to_use_partitioning"><span class="devsite-nav-text" tooltip="">When to use partitioning</span></a></li><li class="devsite-nav-item" visible=""><a href="#types_of_partitioning" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="1" track-type="navigation" track-name="embeddedNav" track-metadata-position="1" track-metadata-link-destination="#types_of_partitioning"><span class="devsite-nav-text" tooltip="">Types of partitioning</span></a><ul class="devsite-nav-list"><li class="devsite-nav-item" visible=""><a href="#integer_range" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="1.0" track-type="navigation" track-name="embeddedNav" track-metadata-position="1.0" track-metadata-link-destination="#integer_range"><span class="devsite-nav-text" tooltip="">Integer range partitioning</span></a></li><li class="devsite-nav-item" visible=""><a href="#date_timestamp_partitioned_tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="1.1" track-type="navigation" track-name="embeddedNav" track-metadata-position="1.1" track-metadata-link-destination="#date_timestamp_partitioned_tables"><span class="devsite-nav-text" tooltip="">Time-unit column partitioning</span></a></li><li class="devsite-nav-item" visible=""><a href="#ingestion_time" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="1.2" track-type="navigation" track-name="embeddedNav" track-metadata-position="1.2" track-metadata-link-destination="#ingestion_time"><span class="devsite-nav-text" tooltip="">Ingestion time partitioning</span></a></li><li class="devsite-nav-item"><a href="#select_daily_hourly_monthly_or_yearly_partitioning" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="1.3" track-type="navigation" track-name="embeddedNav" track-metadata-position="1.3" track-metadata-link-destination="#select_daily_hourly_monthly_or_yearly_partitioning"><span class="devsite-nav-text" tooltip="">Select daily, hourly, monthly, or yearly partitioning</span></a></li></ul></li><li class="devsite-nav-item"><a href="#combining_clustered_and_partitioned_tables" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="2" track-type="navigation" track-name="embeddedNav" track-metadata-position="2" track-metadata-link-destination="#combining_clustered_and_partitioned_tables"><span class="devsite-nav-text" tooltip="">Combining clustered and partitioned tables</span></a></li><li class="devsite-nav-item"><a href="#dt_partition_shard" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="3" track-type="navigation" track-name="embeddedNav" track-metadata-position="3" track-metadata-link-destination="#dt_partition_shard"><span class="devsite-nav-text" tooltip="">Partitioning versus sharding</span></a></li><li class="devsite-nav-item"><a href="#partition_decorators" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="4" track-type="navigation" track-name="embeddedNav" track-metadata-position="4" track-metadata-link-destination="#partition_decorators"><span class="devsite-nav-text" tooltip="">Partition decorators</span></a></li><li class="devsite-nav-item"><a href="#browse-table" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="5" track-type="navigation" track-name="embeddedNav" track-metadata-position="5" track-metadata-link-destination="#browse-table"><span class="devsite-nav-text" tooltip="">Browse the data in a partition</span></a></li><li class="devsite-nav-item"><a href="#export_table_data" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="6" track-type="navigation" track-name="embeddedNav" track-metadata-position="6" track-metadata-link-destination="#export_table_data"><span class="devsite-nav-text" tooltip="">Export table data</span></a></li><li class="devsite-nav-item"><a href="#limitations" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="7" track-type="navigation" track-name="embeddedNav" track-metadata-position="7" track-metadata-link-destination="#limitations"><span class="devsite-nav-text" tooltip="">Limitations</span></a></li><li class="devsite-nav-item"><a href="#quotas_limits" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="8" track-type="navigation" track-name="embeddedNav" track-metadata-position="8" track-metadata-link-destination="#quotas_limits"><span class="devsite-nav-text" tooltip="">Quotas and limits</span></a></li><li class="devsite-nav-item"><a href="#pricing" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="9" track-type="navigation" track-name="embeddedNav" track-metadata-position="9" track-metadata-link-destination="#pricing"><span class="devsite-nav-text" tooltip="">Table pricing</span></a></li><li class="devsite-nav-item"><a href="#table_security" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="10" track-type="navigation" track-name="embeddedNav" track-metadata-position="10" track-metadata-link-destination="#table_security"><span class="devsite-nav-text" tooltip="">Table security</span></a></li><li class="devsite-nav-item"><a href="#whats_next" class="devsite-nav-title gc-analytics-event" data-category="Site-Wide Custom Events" data-action="click" data-label="Embedded nav" data-value="11" track-type="navigation" track-name="embeddedNav" track-metadata-position="11" track-metadata-link-destination="#whats_next"><span class="devsite-nav-text" tooltip="">What's next</span></a></li><li class="devsite-toc-toggle"><button type="button" class="button-flat devsite-nav-more-items material-icons" track-type="navigation" track-name="embeddedNavExpand" title="Expand/collapse contents"></button></li></ul></devsite-toc>
  
    
  <div class="devsite-article-body clearfix
  devsite-no-page-title">

  
    
    
    
    <h1 id="introduction-to-partitioned-tables" data-text="Introduction to partitioned tables" tabindex="-1">Introduction to partitioned tables<div class="devsite-actions" data-nosnippet=""><devsite-feature-tooltip ack-key="AckCollectionsBookmarkTooltipDismiss" analytics-category="Site-Wide Custom Events" analytics-action-show="Callout Profile displayed" analytics-action-close="Callout Profile dismissed" analytics-label="Create Collection Callout" class="devsite-page-bookmark-tooltip nocontent inline-block" dismiss-button="true" id="devsite-collections-dropdown" dismiss-button-text="Dismiss" close-button-text="Got it" rendered="" current-step="0" style="--devsite-popout-offset-x: 32px;">

    
    
      <devsite-bookmark class="show"><devsite-dropdown-list aria-label="Bookmark collections drop down" ellipsis="" checkboxes="" fetchingitems="true" writable="" additemtext="New Collection" rendered="" style="--devsite-popout-offset-x: 0px;"><span data-label="devsite-bookmark-direct-action" data-title="Save page" class="material-icons bookmark-icon bookmark-action" slot="toggle">bookmark_border</span><span data-label="devsite-bookmark-direct-action" data-title="Unsave page" hidden="" class="material-icons bookmark-icon unbookmark-action toggled" slot="toggle">bookmark</span></devsite-dropdown-list></devsite-bookmark>
    

    <span slot="popout-heading">
      
      Stay organized with collections
    </span>
    <span slot="popout-contents">
      
      Save and categorize content based on your preferences.<wbr>
    </span>
  </devsite-feature-tooltip></div></h1>
    

<p>A partitioned table is divided into segments, called partitions, that make it
easier to manage and query your data. By dividing a large table into smaller
partitions, you can improve query performance and control costs by reducing the
number of bytes read by a query. You partition tables by specifying a partition
column which is used to segment the table.</p>

<p>If a query uses a qualifying filter on the value of the partitioning column,
BigQuery can scan the partitions that match the filter and skip
the remaining partitions. This process is called <a href="/bigquery/docs/querying-partitioned-tables">pruning</a>.</p>

<p>In a partitioned table, data is stored in physical blocks, each of which holds
one partition of data. Each partitioned table maintains various metadata about
the sort properties across all operations that modify it. The metadata lets BigQuery
more accurately estimate a query cost before the query is run.</p>
<aside class="note"><strong>Note:</strong><span> The information in
<a href="/bigquery/docs/managing-table-data">Managing table data</a> also applies to
partitioned tables.</span></aside>
<h2 id="when_to_use_partitioning" data-text="When to use partitioning" tabindex="-1" role="presentation"><span class="devsite-heading" role="heading" aria-level="2">When to use partitioning</span><button type="button" class="devsite-heading-link button-flat material-icons" aria-label="Copy link to this section: When to use partitioning" data-title="Copy link to this section: When to use partitioning" data-id="when_to_use_partitioning"></button></h2>

<p>Consider partitioning a table in the following scenarios:</p>

<ul>
<li>You want to improve the query performance by only scanning a portion of a
table.</li>
<li>Your table operation exceeds a <a href="/bigquery/quotas#standard_tables">standard table quota</a> and you can scope the table operations
to specific partition column values allowing higher <a href="/bigquery/quotas#partitioned_tables">partitioned table quotas</a>.</li>
<li>You want to determine query costs before a query runs. BigQuery
provides query cost estimates before the query is run on a partitioned table.
Calculate a query cost estimate by <a href="/bigquery/docs/querying-partitioned-tables">pruning</a>
a partitioned table, then issuing a query dry run to estimate query costs.</li>
<li>You want any of the following partition-level management features:
<ul>
<li><a href="/bigquery/docs/managing-partitioned-tables#partition-expiration">Set a partition expiration time</a> to automatically delete entire partitions
after a specified period of time.</li>
<li><a href="/bigquery/docs/load-data-partitioned-tables#write-to-partition">Write data to a specific partition</a> using load jobs without affecting other partitions in the table.</li>
<li><a href="/bigquery/docs/managing-partitioned-tables#delete_a_partition">Delete specific partitions</a> without scanning the entire table.</li>
</ul></li>
</ul>

<p>Consider <a href="/bigquery/docs/clustered-tables">clustering</a> a table instead of
partitioning a table in the following circumstances:</p>

<ul>
<li>You need more granularity than partitioning allows.</li>
<li>Your queries commonly use filters or aggregation against multiple columns.</li>
<li>The cardinality of the number of values in a column or group of columns is
large.</li>
<li>You don't need strict cost estimates before query execution.</li>
<li>Partitioning results in a small amount of data per partition
(approximately less than 10 GB). Creating many small partitions increases the
table's metadata, and can affect metadata access times when querying the
table.</li>
<li>Partitioning results in a large number of partitions, exceeding the
<a href="/bigquery/quotas#partitioned_tables">limits on partitioned tables</a>.</li>
<li>Your DML operations frequently modify (for example, every few minutes) most
partitions in the table.</li>
</ul>

<p>In such cases, table clustering lets you accelerate queries by clustering
data in specific columns based on user-defined sort properties.</p>

<p>You can also combine clustering and table partitioning to achieve finer-grained
sorting. For more information about this approach, see <a href="#combining_clustered_and_partitioned_tables">Combining clustered and partitioning tables</a>.</p>

<h2 id="types_of_partitioning" data-text="Types of partitioning" tabindex="-1">Types of partitioning</h2>

<p>This section describes the different ways to partition a table.</p>

<h3 id="integer_range" data-text="Integer range partitioning" tabindex="-1">Integer range partitioning</h3>

<p>You can partition a table based on ranges of values in a specific <code translate="no" dir="ltr">INTEGER</code>
column. To create an integer-range partitioned table, you provide:</p>

<ul>
<li>The partitioning column.</li>
<li>The starting value for range partitioning (inclusive).</li>
<li>The ending value for range partitioning (exclusive).</li>
<li>The interval of each range within the partition.</li>
</ul>

<p>For example, suppose you create an integer range partition with the following
specification:</p>

<div class="devsite-table-wrapper"><table>
<thead>
<tr>
<th>Argument</th>
<th>Value</th>
</tr>
</thead>

<tbody>
<tr>
<td>column name</td>
<td><code translate="no" dir="ltr">customer_id</code></td>
</tr>
<tr>
<td>start</td>
<td>0</td>
</tr>
<tr>
<td>end</td>
<td>100</td>
</tr>
<tr>
<td>interval</td>
<td>10</td>
</tr>
</tbody>
</table></div>

<p>The table is partitioned on the <code translate="no" dir="ltr">customer_id</code> column into ranges of interval 10.
The values 0 to 9 go into one partition, values 10 to 19 go into the next
partition, etc., up to 99. Values outside this range go into a partition
named <code translate="no" dir="ltr">__UNPARTITIONED__</code>. Any rows where <code translate="no" dir="ltr">customer_id</code> is <code translate="no" dir="ltr">NULL</code> go into a
partition named <code translate="no" dir="ltr">__NULL__</code>.</p>

<p>For information about integer-range partitioned tables, see
<a href="/bigquery/docs/creating-partitioned-tables#create_an_integer-range_partitioned_table">Create an integer-range partitioned table</a>.</p>

<h3 id="date_timestamp_partitioned_tables" data-text="Time-unit column partitioning" tabindex="-1">Time-unit column partitioning</h3>

<p>You can partition a table on a <code translate="no" dir="ltr">DATE</code>,<code translate="no" dir="ltr">TIMESTAMP</code>, or <code translate="no" dir="ltr">DATETIME</code> column in the
table. When you write data to the table, BigQuery automatically
puts the data into the correct partition, based on the values in the column.</p>

<p>For <code translate="no" dir="ltr">TIMESTAMP</code> and <code translate="no" dir="ltr">DATETIME</code> columns, the partitions can have either hourly,
daily, monthly, or yearly granularity. For <code translate="no" dir="ltr">DATE</code> columns, the partitions can
have daily, monthly, or yearly granularity. Partitions boundaries are based on
UTC time.</p>

<p>For example, suppose that you partition a table on a <code translate="no" dir="ltr">DATETIME</code> column with
monthly partitioning. If you insert the following values into the table, the
rows are written to the following partitions:</p>

<div class="devsite-table-wrapper"><table>
<thead>
<tr>
<th>Column value</th>
<th>Partition (monthly)</th>
</tr>
</thead>

<tbody>
<tr>
<td><code translate="no" dir="ltr">DATETIME("2019-01-01")</code></td>
<td><code translate="no" dir="ltr">201901</code></td>
</tr>
<tr>
<td><code translate="no" dir="ltr">DATETIME("2019-01-15")</code></td>
<td><code translate="no" dir="ltr">201901</code></td>
</tr>
<tr>
<td><code translate="no" dir="ltr">DATETIME("2019-04-30")</code></td>
<td><code translate="no" dir="ltr">201904</code></td>
</tr>
</tbody>
</table></div>

<p>In addition, two special partitions are created:</p>

<ul>
<li><code translate="no" dir="ltr">__NULL__</code>: Contains rows with <code translate="no" dir="ltr">NULL</code> values in the partitioning column.</li>
<li><code translate="no" dir="ltr">__UNPARTITIONED__</code>: Contains rows where the value of the partitioning
column is earlier than 1960-01-01 or later than 2159-12-31.</li>
</ul>

<p>For information about time-unit column-partitioned tables, see
<a href="/bigquery/docs/creating-partitioned-tables#create_a_time-unit_column-partitioned_table">Create a time-unit column-partitioned table</a>.</p>

<h3 id="ingestion_time" data-text="Ingestion time partitioning" tabindex="-1">Ingestion time partitioning</h3>

<p>When you create a table partitioned by ingestion time, BigQuery
automatically assigns rows to partitions based on the time when
BigQuery ingests the data. You can choose hourly, daily, monthly,
or yearly granularity for the partitions. Partitions boundaries are based on UTC
time.</p>

<p>If your data might reach the maximum number of partitions per table when using a
finer time granularity, use a coarser granularity instead. For example, you
can partition by month instead of day to reduce the number of partitions.
You can also <a href="/bigquery/docs/clustered-tables">cluster</a>
the partition column to further improve performance.</p>

<p>An ingestion-time partitioned table has a pseudocolumn named <code translate="no" dir="ltr">_PARTITIONTIME</code>.
The value of this column is the ingestion time for each row, truncated to the
partition boundary (such as hourly or daily). For example, suppose that you
create an ingestion-time partitioned table with hourly partitioning and send
data at the following times:</p>

<div class="devsite-table-wrapper"><table>
<thead>
<tr>
<th>Ingestion time</th>
<th><code translate="no" dir="ltr">_PARTITIONTIME</code></th>
<th>Partition (hourly)</th>
</tr>
</thead>

<tbody>
<tr>
<td>2021-05-07 17:22:00</td>
<td>2021-05-07 17:00:00</td>
<td><code translate="no" dir="ltr">2021050717</code></td>
</tr>
<tr>
<td>2021-05-07 17:40:00</td>
<td>2021-05-07 17:00:00</td>
<td><code translate="no" dir="ltr">2021050717</code></td>
</tr>
<tr>
<td>2021-05-07 18:31:00</td>
<td>2021-05-07 18:00:00</td>
<td><code translate="no" dir="ltr">2021050718</code></td>
</tr>
</tbody>
</table></div>

<p>Because the table in this example uses hourly partitioning, the value of
<code translate="no" dir="ltr">_PARTITIONTIME</code> is truncated to an hour boundary. BigQuery
uses this value to determine the correct partition for the data.</p>

<p>You can also write data to a specific partition. For example, you might want to
load historical data or adjust for time zones. You can use any valid date
between 0001-01-01 and 9999-12-31. However,
<a href="/bigquery/docs/data-manipulation-language">DML statements</a>
cannot reference dates prior to 1970-01-01 or after 2159-12-31. For more
information, see
<a href="/bigquery/docs/load-data-partitioned-tables#write-to-partition">Write data to a specific partition</a>.</p>

<p>Instead of using <code translate="no" dir="ltr">_PARTITIONTIME</code>, you can also use
<a href="/bigquery/docs/querying-partitioned-tables#query_an_ingestion-time_partitioned_table"><code translate="no" dir="ltr">_PARTITIONDATE</code></a>.
The <code translate="no" dir="ltr">_PARTITIONDATE</code> pseudocolumn contains the UTC date corresponding to the value
in the <code translate="no" dir="ltr">_PARTITIONTIME</code> pseudocolumn.</p>

<h3 id="select_daily_hourly_monthly_or_yearly_partitioning" data-text="Select daily, hourly, monthly, or yearly partitioning" tabindex="-1">Select daily, hourly, monthly, or yearly partitioning</h3>

<p>When you partition a table by time-unit column or ingestion time, you choose
whether the partitions have daily, hourly, monthly, or yearly granularity.</p>

<ul>
<li><p><strong>Daily partitioning</strong> is the default partitioning type. Daily partitioning is
a good choice when your data is spread out over a wide range of dates, or if
data is continuously added over time.</p></li>
<li><p>Choose <strong>hourly partitioning</strong> if your tables have a high volume of data
that spans a short date range — typically less than six months of
timestamp values. If you choose hourly partitioning, make sure the partition
count stays within the
<a href="/bigquery/quotas#partitioned_tables">partition limits</a>.</p></li>
<li><p>Choose <strong>monthly or yearly partitioning</strong> if your tables have a relatively
small amount of data for each day, but span a wide date range. This
option is also recommended if your workflow requires frequently updating or
adding rows that span a wide date range (for example, more than 500 dates).
In these scenarios, use monthly or yearly partitioning along with clustering
on the partitioning column to achieve the best performance. For more
information, see
<a href="#combining_clustered_and_partitioned_tables">Combining clustered and partitioning tables</a>
in this document.</p></li>
</ul>

<!-- ### Hashmap partitions and other methods

In some cases, partitions may need to be applied to other column types not
listed above, or there is a need to reduce the number of available values.
In these instances, a few methods are available:

+ Use functions to truncate dates and timestamps to fit within the partition
  value limit.
+ Create a hashmap table storing the non-available keys with an integer lookup,
  then create a partitioned table using the integer key. When querying from the
  partitioned table, use the hashmap table on the query to effectively filter the
  data. -->

<h2 id="combining_clustered_and_partitioned_tables" data-text="Combining clustered and partitioned tables" tabindex="-1">Combining clustered and partitioned tables</h2>

<p>You can combine table partitioning with <a href="/bigquery/docs/clustered-tables">table clustering</a>
to achieve finely grained sorting for further query optimization.</p>

<p>A clustered table contains clustered columns that sort data based on
user-defined sort properties. Data within these clustered columns are sorted
into storage blocks which are adaptively sized based on the size of the table.
When you run a query that filters by the clustered column, BigQuery
only scans the relevant blocks based on the clustered columns instead of the
entire table or table partition. In a combined approach using both table
partitioning and clustering, you first segment table data into partitions,
then you cluster the data within each partition by the clustering columns.</p>

<p>When you create a table that is clustered and partitioned, you can achieve more
finely grained sorting, as the following diagram shows:</p>

<p><img src="/static/bigquery/images/clustering-and-partitioning-tables.png" alt="Comparing tables that are not clustered or partitioned to tables that are clustered and partitioned."></p>

<h2 id="dt_partition_shard" data-text="Partitioning versus sharding" tabindex="-1">Partitioning versus sharding</h2>

<p>Table sharding is the practice of storing data in multiple tables, using a
naming prefix such as <code translate="no" dir="ltr">[PREFIX]_YYYYMMDD</code>.</p>

<p>Partitioning is recommended over table sharding, because partitioned tables
perform better. With sharded tables, BigQuery must maintain a
copy of the schema and metadata for each table. BigQuery might
also need to verify permissions for each queried table. This practice also adds
to query overhead and affects query performance.</p>

<p>If you previously created date-sharded tables, you can convert them into an
ingestion-time partitioned table. For more information, see
<a href="/bigquery/docs/creating-partitioned-tables#convert-date-sharded-tables">Convert date-sharded tables into ingestion-time partitioned tables</a>.</p>

<h2 id="partition_decorators" data-text="Partition decorators" tabindex="-1">Partition decorators</h2>

<p>Partition decorators enable you to reference a partition in a table. For
example, you can use them to
<a href="/bigquery/docs/load-data-partitioned-tables#write-to-partition">write data</a>
to a specific partition.</p>

<p>A partition decorator has the form <code translate="no" dir="ltr">table_name$partition_id</code> where the format
of the <code translate="no" dir="ltr">partition_id</code> segment depends on the type of partitioning:</p>

<div class="devsite-table-wrapper"><table>
<thead>
<tr>
<th>Partitioning type</th>
<th>Format</th>
<th>Example</th>
</tr>
</thead>

<tbody>
<tr>
<td>Hourly</td>
<td><code translate="no" dir="ltr">yyyymmddhh</code></td>
<td><code translate="no" dir="ltr">my_table$2021071205</code></td>
</tr>
<tr>
<td>Daily</td>
<td><code translate="no" dir="ltr">yyyymmdd</code></td>
<td><code translate="no" dir="ltr">my_table$20210712</code></td>
</tr>
<tr>
<td>Monthly</td>
<td><code translate="no" dir="ltr">yyyymm</code></td>
<td><code translate="no" dir="ltr">my_table$202107</code></td>
</tr>
<tr>
<td>Yearly</td>
<td><code translate="no" dir="ltr">yyyy</code></td>
<td><code translate="no" dir="ltr">my_table$2021</code></td>
</tr>
<tr>
<td>Integer range</td>
<td><code translate="no" dir="ltr">range_start</code></td>
<td><code translate="no" dir="ltr">my_table$40</code></td>
</tr>
</tbody>
</table></div>

<h2 id="browse-table" data-text="Browse the data in a partition" tabindex="-1">Browse the data in a partition</h2>

<p>To browse the data in a specified partition, use the
<a href="/bigquery/docs/reference/bq-cli-reference#bq_head"><code translate="no" dir="ltr">bq head</code></a> command with a
partition decorator.</p>

<p>For example, the following command lists all fields in the first 10 rows of
<code translate="no" dir="ltr">my_dataset.my_table</code> in the <code translate="no" dir="ltr">2018-02-24</code> partition:</p>
<div></div><devsite-code data-copy-event-label=""><pre class="" translate="no" dir="ltr" is-upgraded="" syntax="scdoc"><code translate="no" dir="ltr">    bq head --max_rows=10 'my_dataset.my_table$20180224'
</code></pre></devsite-code>
<h2 id="export_table_data" data-text="Export table data" tabindex="-1">Export table data</h2>

<p>Exporting all data from a partitioned table is the same process as exporting
data from a non-partitioned table. For more information, see
<a href="/bigquery/docs/exporting-data">Exporting table data</a>.</p>

<p>To export data from an individual partition, use the <code translate="no" dir="ltr">bq extract</code> command and
append the partition decorator to
the table name. For example, <code translate="no" dir="ltr">my_table$20160201</code>. You can also export data from
the <a href="/bigquery/docs/partitioned-tables#date_timestamp_partitioned_tables"><code translate="no" dir="ltr">__NULL__</code> and <code translate="no" dir="ltr">__UNPARTITIONED__</code></a>
partitions by appending the partition names to the table name. For example,
<code translate="no" dir="ltr">my_table$__NULL__</code> or <code translate="no" dir="ltr">my_table$__UNPARTITIONED__</code>.</p>

<h2 id="limitations" data-text="Limitations" tabindex="-1">Limitations</h2>

<p>You cannot use legacy SQL to query partitioned tables or to write query results
to partitioned tables.</p>

<p>BigQuery does not support partitioning by multiple columns. Only one column can be used to partition a table.</p>

<p>Time-unit column-partitioned tables are subject to the following
limitations:</p>

<ul>
<li>The partitioning column must be either a scalar <code translate="no" dir="ltr">DATE</code>, <code translate="no" dir="ltr">TIMESTAMP</code>, or
<code translate="no" dir="ltr">DATETIME</code> column. While the mode of the column can be <code translate="no" dir="ltr">REQUIRED</code> or
<code translate="no" dir="ltr">NULLABLE</code>, it cannot be <code translate="no" dir="ltr">REPEATED</code> (array-based).</li>
<li>The partitioning column must be a top-level field. You cannot use a leaf field
from a <code translate="no" dir="ltr">RECORD</code> (<code translate="no" dir="ltr">STRUCT</code>) as the partitioning column.</li>
</ul>

<p>For information about time-unit column-partitioned tables, see
<a href="/bigquery/docs/creating-partitioned-tables#create_a_time-unit_column-partitioned_table">Create a time-unit column-partitioned table</a>.</p>

<p>Integer-range partitioned tables are subject to the following limitations:</p>

<ul>
<li>The partitioning column must be an <code translate="no" dir="ltr">INTEGER</code> column. While the mode of the
column may be <code translate="no" dir="ltr">REQUIRED</code> or <code translate="no" dir="ltr">NULLABLE</code>, it cannot be<code translate="no" dir="ltr">REPEATED</code> (array-based).</li>
<li>The partitioning column must be a top-level field. You cannot use a leaf field
from a <code translate="no" dir="ltr">RECORD</code> (<code translate="no" dir="ltr">STRUCT</code>) as the partitioning column.</li>
</ul>

<p>For information about integer-range partitioned tables, see
<a href="/bigquery/docs/creating-partitioned-tables#create_an_integer-range_partitioned_table">Create an integer-range partitioned table</a>.</p>

<h2 id="quotas_limits" data-text="Quotas and limits" tabindex="-1">Quotas and limits</h2>

<p>Partitioned tables have defined <a href="/bigquery/quotas#partitioned_tables">limits</a> in BigQuery.</p>

<p>Quotas and limits also apply to the different types of jobs you can run against
partitioned tables, including:</p>

<ul>
<li><a href="/bigquery/quotas#load_jobs">Loading data</a> (load jobs)</li>
<li><a href="/bigquery/quotas#export_jobs">Exporting data</a> (export jobs)</li>
<li><a href="/bigquery/quotas#query_jobs">Querying data</a> (query jobs)</li>
<li><a href="/bigquery/quotas#copy_jobs">Copying tables</a> (copy jobs)</li>
</ul>

<p>For more information on all quotas and limits, see <a href="/bigquery/quotas">Quotas and limits</a>.</p>

<h2 id="pricing" data-text="Table pricing" tabindex="-1">Table pricing</h2>

<p>When you create and use partitioned tables in BigQuery, your
charges are based on how much data is stored in the partitions and on the
queries you run against the data:</p>

<ul>
<li>For information on storage pricing, see <a href="/bigquery/pricing#storage">Storage pricing</a>.</li>
<li>For information on query pricing, see <a href="/bigquery/pricing#analysis_pricing_models">Query pricing</a>.</li>
</ul>

<p>Many partitioned table operations are free, including loading data into
partitions, copying partitions, and exporting data from partitions. Though free,
these operations are subject to BigQuery's
<a href="/bigquery/quotas">Quotas and limits</a>. For information on all free operations,
see <a href="/bigquery/pricing#free">Free operations</a> on the pricing page.</p>

<p>For best practices for controlling costs in BigQuery, see <a href="/bigquery/docs/best-practices-costs">Controlling costs in BigQuery</a></p>

<h2 id="table_security" data-text="Table security" tabindex="-1">Table security</h2>

<p>Access control for partitioned tables is the same as access control for
standard tables. For more information, see
<a href="/bigquery/docs/table-access-controls-intro">Introduction to table access controls</a>.</p>

<h2 id="whats_next" data-text="What's next" tabindex="-1">What's next</h2>

<ul>
<li>To learn how to create partitioned tables, see
<a href="/bigquery/docs/creating-partitioned-tables">Creating partitioned tables</a>.</li>
<li>To learn how to manage and update partitioned tables, see
<a href="/bigquery/docs/managing-partitioned-tables">Managing partitioned tables</a>.</li>
<li>For information on querying partitioned tables, see
<a href="/bigquery/docs/querying-partitioned-tables">Querying partitioned tables</a>.</li>
</ul>


  
  

  
    <devsite-hats-survey class="nocontent" hats-id="mwETRvWii0eU5NUYprb0Y9z5GVbc" listnr-id="83405"></devsite-hats-survey>
  

  
</div>

  
    
    
      
    <devsite-thumb-rating position="footer"><div class="devsite-thumb-rating" role="form" aria-labelledby="devsite-thumb-label-footer"><div class="devsite-thumb-label" id="devsite-thumb-label-footer">Was this helpful?</div><div class="devsite-thumbs"><button class="devsite-thumb devsite-thumb-up" data-title="Helpful" aria-label="Helpful"><svg class="devsite-thumb-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21,7h-6.31l0.95-4.57l0.03-0.32c0-0.41-0.17-0.79-0.44-1.06L14.17,0c0,0-7.09,6.85-7.17,7H2v13h16 c0.83,0,1.54-0.5,1.84-1.22l3.02-7.05C22.95,11.5,23,11.26,23,11V9C23,7.9,22.1,7,21,7z M7,18H4V9h3V18z M21,11l-3,7H9V8l4.34-4.34 L12,9h9V11z"></path></svg></button><button class="devsite-thumb devsite-thumb-down" data-title="Not helpful" aria-label="Not helpful"><svg class="devsite-thumb-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3,17h6.31l-0.95,4.57l-0.03,0.32c0,0.41,0.17,0.79,0.44,1.06L9.83,24c0,0,7.09-6.85,7.17-7h5V4H6 C5.17,4,4.46,4.5,4.16,5.22l-3.02,7.05C1.05,12.5,1,12.74,1,13v2C1,16.1,1.9,17,3,17z M17,6h3v9h-3V6z M3,13l3-7h9v10l-4.34,4.34 L12,15H3V13z"></path></svg></button></div></div></devsite-thumb-rating>
  
       
         <devsite-feedback position="footer" project-name="BigQuery" product-id="81912" bucket="docs" context="" version="t-devsite-webserver-20250805-r00-rc04.471103249751607376" data-label="Send Feedback Button" track-type="feedback" track-name="sendFeedbackLink" track-metadata-position="footer" class="nocontent" project-feedback-url="https://issuetracker.google.com/issues/new?component=187149&amp;template=0" project-icon="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/favicons/onecloud/super_cloud.png" project-support-url="https://cloud.google.com/bigquery/docs/getting-support">

  <button>
  
    
    Send feedback
  
  </button>
</devsite-feedback>
       
    
    
  

  <div class="devsite-floating-action-buttons"></div></article>


<devsite-content-footer class="nocontent">
  <p>Except as otherwise noted, the content of this page is licensed under the <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 License</a>, and code samples are licensed under the <a href="https://www.apache.org/licenses/LICENSE-2.0">Apache 2.0 License</a>. For details, see the <a href="https://developers.google.com/site-policies">Google Developers Site Policies</a>. Java is a registered trademark of Oracle and/or its affiliates.</p>
  <p>Last updated 2025-08-07 UTC.</p>
</devsite-content-footer>


<devsite-notification>
</devsite-notification>


  
<div class="devsite-content-data">
  
    
    
    <template class="devsite-thumb-rating-feedback">
      <devsite-feedback position="thumb-rating" project-name="BigQuery" product-id="81912" bucket="docs" context="" version="t-devsite-webserver-20250805-r00-rc04.471103249751607376" data-label="Send Feedback Button" track-type="feedback" track-name="sendFeedbackLink" track-metadata-position="thumb-rating" class="nocontent" project-feedback-url="https://issuetracker.google.com/issues/new?component=187149&amp;template=0" project-icon="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/favicons/onecloud/super_cloud.png" project-support-url="https://cloud.google.com/bigquery/docs/getting-support">

  <button>
  
    Need to tell us more?
  
  </button>
</devsite-feedback>
    </template>
  
  
    <template class="devsite-content-data-template">
      [[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-08-07 UTC."],[[["Partitioned tables divide large datasets into smaller, more manageable segments called partitions, improving query performance and reducing costs by limiting the amount of data scanned."],["Partitioning a table is advantageous when you want to enhance query speeds, manage table operations within specific partition quotas, estimate query costs beforehand, and utilize partition-level management features."],["There are three types of partitioning methods: integer range, time-unit column (using `DATE`, `TIMESTAMP`, or `DATETIME` columns), and ingestion time, each offering different ways to segment data."],["Clustering can be used instead of partitioning when finer granularity is needed or when dealing with queries that filter or aggregate across multiple columns, and partitioning can also be combined with clustering for more optimized sorting."],["Partitioning is preferred over table sharding because partitioned tables offer better performance and lower overhead, as they eliminate the need to manage schemas and permissions for multiple tables separately."]]],[]]
    </template>
  
</div>
            
          </devsite-content>
        </main>
        <devsite-footer-promos class="devsite-footer">
          
            
          
        </devsite-footer-promos>
        <devsite-footer-linkboxes class="devsite-footer">
          
            
<nav class="devsite-footer-linkboxes nocontent" aria-label="Footer links">
  
  <ul class="devsite-footer-linkboxes-list">
    
    <li class="devsite-footer-linkbox ">
    <h3 class="devsite-footer-linkbox-heading no-link">Why Google</h3>
      <ul class="devsite-footer-linkbox-list">
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/why-google-cloud/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 1)" track-name="choosing google cloud" track-type="footer link" track-metadata-module="footer" track-metadata-eventdetail="cloud.google.com/why-google-cloud/" track-metadata-position="footer" track-metadata-child_headline="why google">
            
          
            Choosing Google Cloud
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/trust-center/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 2)" track-metadata-module="footer" track-name="trust and security" track-metadata-eventdetail="cloud.google.com/security/" track-metadata-position="footer" track-type="footer link" track-metadata-child_headline="why google">
            
          
            Trust and security
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/solutions/modern-infrastructure/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 3)" track-metadata-module="footer" track-metadata-eventdetail="cloud.google.com/solutions/modern-infrastructure/" track-metadata-child_headline="why google" track-metadata-position="footer" track-type="footer link" track-name="modern infrastructure cloud">
            
          
            Modern Infrastructure Cloud
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/multicloud/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 4)" track-type="footer link" track-metadata-module="footer" track-metadata-eventdetail="cloud.google.com/multicloud/" track-metadata-position="footer" track-metadata-child_headline="why google" track-name="multicloud">
            
          
            Multicloud
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/infrastructure/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 5)" track-metadata-module="footer" track-metadata-position="footer" track-metadata-eventdetail="cloud.google.com/infrastructure/" track-metadata-child_headline="why google" track-type="footer link" track-name="global infrastructure">
            
          
            Global infrastructure
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/customers/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 6)" track-metadata-position="footer" track-type="footer link" track-metadata-child_headline="why google" track-metadata-module="footer" track-name="customers and case studies" track-metadata-eventdetail="cloud.google.com/customers/">
            
          
            Customers and case studies
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/analyst-reports/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 7)" track-name="analyst reports" track-metadata-position="footer" track-metadata-eventdetail="cloud.google.com/analyst-reports/" track-metadata-child_headline="why google" track-type="footer link" track-metadata-module="footer">
            
          
            Analyst reports
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/whitepapers/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 8)" track-metadata-module="footer" track-name="whitepapers" track-type="footer link" track-metadata-position="footer" track-metadata-eventdetail="cloud.google.com/whitepapers/" track-metadata-child_headline="why google">
            
              
              
            
          
            Whitepapers
          
          </a>
          
          
        </li>
        
      </ul>
    </li>
    
    <li class="devsite-footer-linkbox ">
    <h3 class="devsite-footer-linkbox-heading no-link">Products and pricing</h3>
      <ul class="devsite-footer-linkbox-list">
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/products/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 1)" track-name="see all products" track-metadata-module="footer" track-metadata-eventdetail="cloud.google.com/products/" track-metadata-child_headline="products and pricing" track-metadata-position="footer" track-type="footer link">
            
          
            See all products
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/solutions/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 2)" track-metadata-child_headline="solutions" track-metadata-position="footer" track-metadata-eventdetail="cloud.google.com/solutions/" track-type="footer link" track-name="see all solutions" track-metadata-module="footer">
            
          
            See all solutions
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/startup/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 3)" track-metadata-eventdetail="cloud.google.com/startup/" track-metadata-child_headline="resources" track-metadata-module="footer" track-name="google cloud for startups" track-metadata-position="footer" track-type="footer link">
            
          
            Google Cloud for Startups
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/marketplace/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 4)" track-name="google cloud marketplace" track-metadata-eventdetail="cloud.google.com/marketplace/" track-metadata-child_headline="resources" track-metadata-module="footer" track-metadata-position="footer" track-type="footer link">
            
          
            Google Cloud Marketplace
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/pricing/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 5)" track-name="google cloud pricing" track-type="footer link" track-metadata-child_headline="products and pricing" track-metadata-position="footer" track-metadata-eventdetail="cloud.google.com/pricing/" track-metadata-module="footer">
            
          
            Google Cloud pricing
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/contact/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 6)" track-metadata-eventdetail="cloud.google.com/contact/" track-metadata-module="footer" track-metadata-child_headline="engage" track-metadata-position="footer" track-type="footer link" track-name="contact sales">
            
              
              
            
          
            Contact sales
          
          </a>
          
          
        </li>
        
      </ul>
    </li>
    
    <li class="devsite-footer-linkbox ">
    <h3 class="devsite-footer-linkbox-heading no-link">Support</h3>
      <ul class="devsite-footer-linkbox-list">
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//www.googlecloudcommunity.com/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 1)" track-type="footer link" target="_blank" track-metadata-module="footer" track-name="google cloud community" track-metadata-child_headline="engage" rel="noopener" track-metadata-position="footer" track-metadata-eventdetail="www.googlecloudcommunity.com">
            
          
            Google Cloud Community
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/support-hub/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 2)" track-metadata-position="footer" track-type="footer link" track-metadata-module="footer" track-metadata-child_headline="resources" track-metadata-eventdetail="cloud.google.com/support-hub/" track-name="support">
            
          
            Support
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/release-notes" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 3)" track-metadata-eventdetail="cloud.google.com/release-notes/" track-type="footer link" track-metadata-child_headline="resources" track-metadata-module="footer" track-metadata-position="footer" track-name="release notes">
            
          
            Release Notes
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//status.cloud.google.com" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 4)" track-metadata-position="footer" track-metadata-eventdetail="status.cloud.google.com" track-metadata-child_headline="resources" target="_blank" track-name="system status" track-type="footer link" track-metadata-module="footer">
            
              
              
            
          
            System status
          
          </a>
          
          
        </li>
        
      </ul>
    </li>
    
    <li class="devsite-footer-linkbox ">
    <h3 class="devsite-footer-linkbox-heading no-link">Resources</h3>
      <ul class="devsite-footer-linkbox-list">
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//github.com/googlecloudPlatform/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 1)" track-type="footer link" track-metadata-module="footer" track-metadata-position="footer" track-metadata-eventdetail="github.com/googlecloudPlatform/" track-name="github" track-metadata-child_headline="resources">
            
          
            GitHub
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/docs/get-started/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 2)" track-name="google cloud quickstarts" track-metadata-position="footer" track-metadata-module="footer" track-metadata-child_headline="resources" track-type="footer link" track-metadata-eventdetail="cloud.google.com/docs/get-started/">
            
          
            Getting Started with Google Cloud
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/docs/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 3)" track-metadata-position="footer" track-type="footer link" track-metadata-module="footer" track-metadata-eventdetail="cloud.google.com/docs/" track-name="google cloud documentation" track-metadata-child_headline="resources">
            
          
            Google Cloud documentation
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/docs/samples" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 4)" track-metadata-child_headline="resources" track-type="footer link" track-metadata-eventdetail="cloud.google.com/docs/samples" track-name="code samples" track-metadata-module="footer" track-metadata-position="footer">
            
          
            Code samples
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/architecture/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 5)" track-metadata-module="footer" track-metadata-child_headline="resources" track-name="cloud architecture center" track-metadata-eventdetail="cloud.google.com/architecture/" track-metadata-position="footer" track-type="footer link">
            
          
            Cloud Architecture Center
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//cloud.google.com/learn/training/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 6)" track-metadata-eventdetail="cloud.google.com/learn/training/" track-name="training" track-metadata-child_headline="resources" track-metadata-module="footer" track-type="footer link" track-metadata-position="footer">
            
          
            Training and Certification
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/developers/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 7)" track-metadata-module="footer" track-metadata-position="footer" track-metadata-eventdetail="cloud.google.com/developers/" track-type="footer link" track-name="developer center" track-metadata-child_headline="engage">
            
              
              
            
          
            Developer Center
          
          </a>
          
          
        </li>
        
      </ul>
    </li>
    
    <li class="devsite-footer-linkbox ">
    <h3 class="devsite-footer-linkbox-heading no-link">Engage</h3>
      <ul class="devsite-footer-linkbox-list">
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//cloud.google.com/blog/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 1)" track-type="footer link" track-metadata-eventdetail="cloud.google.com/blog/" track-metadata-child_headline="engage" track-metadata-module="footer" track-metadata-position="footer" track-name="blog">
            
          
            Blog
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/events/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 2)" track-name="events" track-metadata-module="footer" track-metadata-eventdetail="cloud.google.com/events/" track-metadata-position="footer" track-type="footer link" track-metadata-child_headline="engage">
            
          
            Events
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//x.com/googlecloud" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 3)" track-type="footer link" track-metadata-eventdetail="x.com/googlecloud" target="_blank" rel="noopener" track-metadata-child_headline="engage" track-name="follow on x" track-metadata-position="footer" track-metadata-module="footer">
            
          
            X (Twitter)
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//www.youtube.com/googlecloud" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 4)" target="_blank" rel="noopener" track-metadata-eventdetail="www.youtube.com/googlecloud" track-metadata-child_headline="engage" track-name="google cloud on youtube" track-metadata-module="footer" track-type="footer link" track-metadata-position="footer">
            
          
            Google Cloud on YouTube
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//www.youtube.com/googlecloudplatform" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 5)" rel="noopener" track-metadata-eventdetail="www.youtube.com/googlecloudplatform" track-metadata-child_headline="engage" target="_blank" track-type="footer link" track-metadata-position="footer" track-metadata-module="footer" track-name="google cloud tech on youtube">
            
          
            Google Cloud Tech on YouTube
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/partners/become-a-partner/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 6)" track-metadata-child_headline="engage" track-name="become a partner" track-metadata-position="footer" track-metadata-eventdetail="cloud.google.com/partners/become-a-partner/" track-type="footer link" track-metadata-module="footer">
            
          
            Become a Partner
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="/affiliate-program/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 7)" track-metadata-module="footer" track-name="google cloud affiliate program" track-metadata-eventdetail="cloud.google.com/affiliate-program/" track-type="footer link" track-metadata-position="footer" track-metadata-child_headline="resources">
            
          
            Google Cloud Affiliate Program
          
          </a>
          
          
        </li>
        
        <li class="devsite-footer-linkbox-item">
          
          <a href="//www.googlecloudpresscorner.com/" class="devsite-footer-linkbox-link gc-analytics-event" data-category="Site-Wide Custom Events" data-label="Footer Link (index 8)" target="_blank" track-name="press corner" track-metadata-module="footer" track-metadata-eventdetail="www.googlecloudpresscorner.com" rel="noopener" track-type="footer link" track-metadata-child_headline="engage" track-metadata-position="footer">
            
              
              
            
          
            Press Corner
          
          </a>
          
          
        </li>
        
      </ul>
    </li>
    
  </ul>
  
</nav>
          
        </devsite-footer-linkboxes>
        <devsite-footer-utility class="devsite-footer">
          
            

<div class="devsite-footer-utility nocontent">
  

  
  <nav class="devsite-footer-utility-links" aria-label="Utility links">
    
    <ul class="devsite-footer-utility-list">
      
      <li class="devsite-footer-utility-item
                 ">
        
        
        <a class="devsite-footer-utility-link gc-analytics-event" href="//about.google/" data-category="Site-Wide Custom Events" data-label="Footer About Google link" track-metadata-eventdetail="//about.google/" track-metadata-module="utility footer" target="_blank" track-metadata-position="footer" track-type="footer link" track-name="about google">
          About Google
        </a>
        
      </li>
      
      <li class="devsite-footer-utility-item
                 devsite-footer-privacy-link">
        
        
        <a class="devsite-footer-utility-link gc-analytics-event" href="//policies.google.com/privacy" data-category="Site-Wide Custom Events" data-label="Footer Privacy link" track-metadata-module="utility footer" target="_blank" track-metadata-eventdetail="//policies.google.com/privacy" track-metadata-position="footer" track-type="footer link" track-name="privacy">
          Privacy
        </a>
        
      </li>
      
      <li class="devsite-footer-utility-item
                 ">
        
        
        <a class="devsite-footer-utility-link gc-analytics-event" href="//policies.google.com/terms?hl=en" data-category="Site-Wide Custom Events" data-label="Footer Site terms link" track-metadata-position="footer" track-name="site terms" target="_blank" track-metadata-eventdetail="//www.google.com/intl/en/policies/terms/regional.html" track-type="footer link" track-metadata-module="utility footer">
          Site terms
        </a>
        
      </li>
      
      <li class="devsite-footer-utility-item
                 ">
        
        
        <a class="devsite-footer-utility-link gc-analytics-event" href="/product-terms/" data-category="Site-Wide Custom Events" data-label="Footer Google Cloud terms link" track-type="footer link" track-metadata-position="footer" track-name="google cloud terms" track-metadata-eventdetail="/product-terms/" track-metadata-module="utility footer">
          Google Cloud terms
        </a>
        
      </li>
      
      <li class="devsite-footer-utility-item
                 glue-cookie-notification-bar-control">
        
        
        <a class="devsite-footer-utility-link gc-analytics-event" href="#" data-category="Site-Wide Custom Events" data-label="Footer Manage cookies link" track-metadata-position="footer" track-name="Manage cookies" track-type="footer link" track-metadata-eventdetail="#" track-metadata-module="utility footer" aria-hidden="true">
          Manage cookies
        </a>
        
      </li>
      
      <li class="devsite-footer-utility-item
                 devsite-footer-carbon-button">
        
        
        <a class="devsite-footer-utility-link gc-analytics-event" href="//cloud.google.com/sustainability" data-category="Site-Wide Custom Events" data-label="Footer Our third decade of climate action: join us link" track-name="Our third decade of climate action: join us" track-metadata-module="utility footer" track-metadata-position="footer" track-type="footer link" track-metadata-eventdetail="/sustainability/">
          Our third decade of climate action: join us
        </a>
        
      </li>
      
      <li class="devsite-footer-utility-item
                 devsite-footer-utility-button">
        
        <span class="devsite-footer-utility-description">Sign up for the Google Cloud newsletter</span>
        
        
        <a class="devsite-footer-utility-link gc-analytics-event" href="//cloud.google.com/newsletter/" data-category="Site-Wide Custom Events" data-label="Footer Subscribe link" track-metadata-position="footer" track-metadata-eventdetail="/newsletter/" track-name="subscribe" track-metadata-module="utility footer" track-type="footer link">
          Subscribe
        </a>
        
      </li>
      
    </ul>
    
    
<devsite-language-selector aria-label="Select your language preference.">
  <ul role="presentation">
    
    
    <li role="presentation">
      <a role="menuitem" lang="en" aria-current="true" href="https://cloud.google.com/bigquery/docs/partitioned-tables">English</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="de" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=de">Deutsch</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="es-419" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=es-419">Español – América Latina</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="fr" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=fr">Français</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="pt-br" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=pt-br">Português – Brasil</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="zh-cn" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-cn">中文 – 简体</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="ja" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=ja">日本語</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="ko" href="https://cloud.google.com/bigquery/docs/partitioned-tables?hl=ko">한국어</a>
    </li>
    
  </ul>
</devsite-language-selector>

  </nav>
</div>
          
        </devsite-footer-utility>
        <devsite-panel height-visual-offset="24" always-on-top="" style="height: auto;">
          
<cloud-shell-pane always-on-top="" enable-fte-user-flow="" height-visual-offset="24">
<!---->
    <div class="resizer" role="separator" aria-valuemin="0" aria-valuemax="0">
      <div class="grabber-focus">
        <div class="grabber"></div>
      </div>
    </div>
    <devsite-shell>
    </devsite-shell>
    <!--?lit$118760000$--> <div class="free-trial-banner">
    <a class="close-btn button-white material-icons" aria-label="Close Cloud Shell">close</a>
    <div class="banner-text">
      <h3><!--?lit$118760000$-->Welcome to Cloud Shell</h3>
      <p><!--?lit$118760000$-->Cloud Shell is a development environment that you can use in the browser:</p>
      <ul>
        <li><!--?lit$118760000$-->Activate Cloud Shell to explore Google Cloud with a terminal and an editor</li>
        <li><!--?lit$118760000$-->Start a free trial to get $300 in free credits</li>
      </ul>
      <div class="row">
        <button class="button-blue"><!--?lit$118760000$-->Activate Cloud Shell
        </button>
        <button>
          <!--?lit$118760000$-->Start a free trial</button>
      </div>
    </div>
    <!--?lit$118760000$--><img src="https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/images/cloud-shell-cta-art.png">
  </div>
  </cloud-shell-pane>

        </devsite-panel>
        
      </section></section>
    <devsite-sitemask></devsite-sitemask>
    <devsite-snackbar style="bottom: 0px;"></devsite-snackbar>
    <devsite-tooltip></devsite-tooltip>
    <devsite-heading-link></devsite-heading-link>
    <devsite-analytics>
      
        <script type="application/json" analytics="">[]</script>
<script type="application/json" tag-management="">{&#34;at&#34;: &#34;True&#34;, &#34;ga4&#34;: [], &#34;ga4p&#34;: [], &#34;gtm&#34;: [{&#34;id&#34;: &#34;GTM-5CVQBG&#34;, &#34;purpose&#34;: 1}], &#34;parameters&#34;: {&#34;internalUser&#34;: &#34;False&#34;, &#34;language&#34;: {&#34;machineTranslated&#34;: &#34;False&#34;, &#34;requested&#34;: &#34;en&#34;, &#34;served&#34;: &#34;en&#34;}, &#34;pageType&#34;: &#34;article&#34;, &#34;projectName&#34;: &#34;BigQuery&#34;, &#34;signedIn&#34;: &#34;True&#34;, &#34;tenant&#34;: &#34;cloud&#34;, &#34;recommendations&#34;: {&#34;sourcePage&#34;: &#34;&#34;, &#34;sourceType&#34;: 0, &#34;sourceRank&#34;: 0, &#34;sourceIdenticalDescriptions&#34;: 0, &#34;sourceTitleWords&#34;: 0, &#34;sourceDescriptionWords&#34;: 0, &#34;experiment&#34;: &#34;&#34;}, &#34;experiment&#34;: {&#34;ids&#34;: &#34;&#34;}}}</script>
      
    </devsite-analytics>
    
      <devsite-badger></devsite-badger>
    
    
    <cloudx-user></cloudx-user>


  <cloudx-free-trial-eligible-store freetrialeligible="false"></cloudx-free-trial-eligible-store>


<cloudx-pricing-socket></cloudx-pricing-socket>
<cloudx-experiments type="TestAACodivertedExperiment" path="/virtual/TestAACodivertedExperiment/configureExperiment" location="US" variant="variant1"></cloudx-experiments>
<cloudx-experiment-ids usercountry="US" devsiteexperimentidlist="[39300013, 39300020, 39300118, 39300196, 39300251, 39300319, 39300320, 39300326, 39300345, 39300354, 39300363, 39300373, 39300409, 39300421, 39300435, 39300471, 39300488, 39300496, 39300498, 39300569, 39300623]">
</cloudx-experiment-ids>
    
<script nonce="">
  
  (function(d,e,v,s,i,t,E){d['GoogleDevelopersObject']=i;
    t=e.createElement(v);t.async=1;t.src=s;E=e.getElementsByTagName(v)[0];
    E.parentNode.insertBefore(t,E);})(window, document, 'script',
    'https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/app_loader.js', '[2,"en",null,"/js/devsite_app_module.js","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud","https://cloud-dot-devsite-v2-prod.appspot.com",null,null,["/_pwa/cloud/manifest.json","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/images/video-placeholder.svg","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/favicons/onecloud/favicon.ico","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/cloud-logo.svg","https://fonts.googleapis.com/css?family=Google+Sans:400,500,700|Google+Sans+Text:400,400italic,500,500italic,700,700italic|Roboto:400,400italic,500,500italic,700,700italic|Roboto+Mono:400,500,700&display=swap"],1,null,[1,6,8,12,14,17,21,25,50,52,63,70,75,76,80,87,91,92,93,97,98,100,101,102,103,104,105,107,108,109,110,112,113,117,118,120,122,124,125,126,127,129,130,131,132,133,134,135,136,138,140,141,147,148,149,151,152,156,157,158,159,161,163,164,168,169,170,179,180,182,183,186,191,193,196],"AIzaSyAP-jjEJBzmIyKR4F-3XITp8yM9T1gEEI8","AIzaSyB6xiKGDR5O3Ak2okS4rLkauxGUG7XP0hg","cloud.google.com","AIzaSyAQk0fBONSGUqCNznf6Krs82Ap1-NV6J4o","AIzaSyCCxcqdrZ_7QMeLCRY20bh_SXdAYqy70KY",null,null,null,["Concierge__enable_actions_menu","EngEduTelemetry__enable_engedu_telemetry","MiscFeatureFlags__emergency_css","DevPro__enable_google_payments","MiscFeatureFlags__developers_footer_image","Cloud__enable_cloud_dlp_service","MiscFeatureFlags__enable_appearance_cookies","Search__enable_ai_search_summaries","DevPro__enable_google_payments_buyflow","DevPro__enable_devpro_offers","DevPro__enable_code_assist","Profiles__require_profile_eligibility_for_signin","MiscFeatureFlags__gdp_dashboard_reskin_enabled","TpcFeatures__proxy_prod_host","Search__enable_page_map","Search__enable_suggestions_from_borg","Profiles__enable_release_notes_notifications","Profiles__enable_purchase_prompts","CloudShell__cloud_code_overflow_menu","Profiles__enable_join_program_group_endpoint","DevPro__enable_cloud_innovators_plus","Concierge__enable_concierge_restricted","DevPro__enable_embed_profile_creation","Cloud__enable_free_trial_server_call","Experiments__reqs_query_experiments","DevPro__enable_vertex_credit_card","Profiles__enable_complete_playlist_endpoint","Profiles__enable_public_developer_profiles","MiscFeatureFlags__enable_view_transitions","Profiles__enable_completecodelab_endpoint","Cloud__enable_cloud_shell","Profiles__enable_profile_collections","Profiles__enable_user_type","Profiles__enable_developer_profiles_callout","Profiles__enable_playlist_community_acl","Search__enable_ai_search_summaries_restricted","Cloud__fast_free_trial","CloudShell__cloud_shell_button","DevPro__enable_nvidia_credits_card","DevPro__enable_firebase_workspaces_card","DevPro__enable_free_benefits","DevPro__enable_google_one_card","Concierge__enable_remove_info_panel_tags","BookNav__enable_tenant_cache_key","MiscFeatureFlags__enable_variable_operator","MiscFeatureFlags__enable_project_variables","Concierge__enable_tutorial_this_code","Cloud__enable_cloudx_experiment_ids","Profiles__enable_dashboard_curated_recommendations","Profiles__enable_recognition_badges","Concierge__enable_pushui","MiscFeatureFlags__developers_footer_dark_image","Cloud__cache_serialized_dynamic_content","TpcFeatures__enable_unmirrored_page_left_nav","MiscFeatureFlags__enable_explicit_template_dependencies","MiscFeatureFlags__enable_framebox_badge_methods","Cloud__enable_legacy_calculator_redirect","Profiles__enable_stripe_subscription_management","Cloud__enable_llm_concierge_chat","Search__enable_ai_search_summaries_for_all","Search__scope_to_project_tenant","DevPro__remove_eu_tax_intake_form","DevPro__enable_developer_subscriptions","Profiles__enable_awarding_url","Profiles__enable_callout_notifications","Search__enable_ai_eligibility_checks","Search__enable_dynamic_content_confidential_banner","Analytics__enable_clearcut_logging","MiscFeatureFlags__enable_explain_this_code","Profiles__enable_developer_profile_benefits_ui_redesign","MiscFeatureFlags__enable_variable_operator_index_yaml","Cloud__enable_cloud_shell_fte_user_flow","MiscFeatureFlags__enable_firebase_utm","Profiles__enable_page_saving","DevPro__enable_enterprise"],null,null,"AIzaSyBLEMok-5suZ67qRPzx0qUtbnLmyT_kCVE","https://developerscontentserving-pa.clients6.google.com","AIzaSyCM4QpTRSqP5qI4Dvjt4OAScIN8sOUlO-k","https://developerscontentsearch-pa.clients6.google.com",1,4,1,"https://developerprofiles-pa.clients6.google.com",[2,"cloud","Google Cloud","cloud.google.com",null,"cloud-dot-devsite-v2-prod.appspot.com",null,null,[1,1,null,null,null,null,null,null,null,null,null,[1],null,null,null,null,null,1,[1],[null,null,null,[1,20],"/terms/recommendations"],[1],null,[1],[1,null,1],[1,1,null,null,1,null,["/vertex-ai/"]],[1]],null,[22,null,null,null,null,null,"/images/cloud-logo.svg","/images/favicons/onecloud/apple-icon.png",null,null,null,null,1,1,1,[6,5],[],null,null,[[],[],[],[],[],[],[],[]],null,null,null,null,null,null,[]],[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[6,1,14,15,22,23,29,37],null,[[null,null,null,null,null,null,[1,[["docType","Choose a content type",[["ApiReference",null,null,null,null,null,null,null,null,"API reference"],["Sample",null,null,null,null,null,null,null,null,"Code sample"],["ReferenceArchitecture",null,null,null,null,null,null,null,null,"Reference architecture"],["Tutorial",null,null,null,null,null,null,null,null,"Tutorial"]]],["category","Choose a topic",[["AiAndMachineLearning",null,null,null,null,null,null,null,null,"Artificial intelligence and machine learning (AI/ML)"],["ApplicationDevelopment",null,null,null,null,null,null,null,null,"Application development"],["BigDataAndAnalytics",null,null,null,null,null,null,null,null,"Big data and analytics"],["Compute",null,null,null,null,null,null,null,null,"Compute"],["Containers",null,null,null,null,null,null,null,null,"Containers"],["Databases",null,null,null,null,null,null,null,null,"Databases"],["HybridCloud",null,null,null,null,null,null,null,null,"Hybrid and multicloud"],["LoggingAndMonitoring",null,null,null,null,null,null,null,null,"Logging and monitoring"],["Migrations",null,null,null,null,null,null,null,null,"Migrations"],["Networking",null,null,null,null,null,null,null,null,"Networking"],["SecurityAndCompliance",null,null,null,null,null,null,null,null,"Security and compliance"],["Serverless",null,null,null,null,null,null,null,null,"Serverless"],["Storage",null,null,null,null,null,null,null,null,"Storage"]]]]]],[1],null,1],[[null,null,null,null,null,["GTM-5CVQBG"],null,null,null,null,null,[["GTM-5CVQBG",2]],1],null,null,null,null,null,1],"mwETRvWii0eU5NUYprb0Y9z5GVbc",4,null,null,null,null,null,null,null,null,null,null,null,null,null,"cloud.devsite.google"],null,"pk_live_5170syrHvgGVmSx9sBrnWtA5luvk9BwnVcvIi7HizpwauFG96WedXsuXh790rtij9AmGllqPtMLfhe2RSwD6Pn38V00uBCydV4m",1,1,"https://developerscontentinsights-pa.clients6.google.com","AIzaSyCg-ZUslalsEbXMfIo9ZP8qufZgo3LSBDU","AIzaSyDxT0vkxnY_KeINtA4LSePJO-4MAZPMRsE","https://developers.clients6.google.com"]')
  
</script>

    <devsite-a11y-announce aria-live="assertive" aria-atomic="true"></devsite-a11y-announce>
  
<iframe id="apiproxy92e1874c28f066c95a8d6bd7909a07ca3d858fed0.3174729133" name="apiproxy92e1874c28f066c95a8d6bd7909a07ca3d858fed0.3174729133" src="https://feedback-pa.clients6.google.com/static/proxy.html?usegapi=1&amp;jsh=m%3B%2F_%2Fscs%2Fabc-static%2F_%2Fjs%2Fk%3Dgapi.lb.en.PLtFj_-5DjQ.O%2Fd%3D1%2Frs%3DAHpOoo-J85zQk73PCqZPyWTydWEIq3_4KA%2Fm%3D__features__#parent=https%3A%2F%2Fcloud.google.com&amp;rpctoken=1582101303" tabindex="-1" aria-hidden="true" style="width: 1px; height: 1px; position: absolute; top: -100px; display: none;"></iframe><iframe height="0" width="0" style="display: none; visibility: hidden;"></iframe><iframe allow="join-ad-interest-group" data-tagging-id="DC-2507573/cloud/googl003+unique" data-load-time="1755363734529" height="0" width="0" src="https://td.doubleclick.net/td/fls/rul/activityi;fledge=1;src=2507573;type=cloud;cat=googl003;ord=1;num=8331665758825;npa=0;auiddc=1703008205.1751311484;uaa=x86;uab=64;uafvl=Not)A%253BBrand%3B8.0.0.0%7CChromium%3B138.0.7204.184%7CGoogle%2520Chrome%3B138.0.7204.184;uamb=0;uam=;uap=Windows;uapv=19.0.0;uaw=0;pscdl=noapi;frm=0;_tu=KpA;gtm=45fe58d1v9181638614z89175119176za200zb9175119176zd6343254;gcs=G111;gcd=13r3r3l3l5l1;dma=0;dc_fmt=9;tag_exp=101509157~103116026~103200004~103233427~104527907~104528501~104684208~104684211~104948813~105033763~105033765~105103161~105103163~105231383~105231385;dc_random=-rJNXmGfmfOyrPC3RrhjI_g3-AnBci_vSg;_dc_test=1;epver=2?" style="display: none; visibility: hidden;"></iframe><iframe allow="join-ad-interest-group" data-tagging-id="DC-2507573/cloud/enter006+standard" data-load-time="1755363734532" height="0" width="0" src="https://td.doubleclick.net/td/fls/rul/activityi;fledge=1;src=2507573;type=cloud;cat=enter006;ord=4709831372866;npa=0;auiddc=1703008205.1751311484;uaa=x86;uab=64;uafvl=Not)A%253BBrand%3B8.0.0.0%7CChromium%3B138.0.7204.184%7CGoogle%2520Chrome%3B138.0.7204.184;uamb=0;uam=;uap=Windows;uapv=19.0.0;uaw=0;pscdl=noapi;frm=0;_tu=KlA;gtm=45fe58d1v9181638614z89175119176za200zb9175119176zd6343254;gcs=G111;gcd=13r3r3l3l5l1;dma=0;dc_fmt=9;tag_exp=101509157~103116026~103200004~103233427~104527907~104528501~104684208~104684211~104948813~105033763~105033765~105103161~105103163~105231383~105231385;dc_random=Xiu0oXFQCh4PP0st-YLggHUEMcCISddOag;_dc_test=1;epver=2?" style="display: none; visibility: hidden;"></iframe><iframe id="hfcr" src="https://accounts.google.com/RotateCookiesPage?og_pid=331&amp;rot=3&amp;origin=https%3A%2F%2Fcloud.google.com&amp;exp_id=0" style="display: none;"></iframe></body></html>