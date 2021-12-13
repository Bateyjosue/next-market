// $('.pointing .menu .item')
//     .tab({
//     cache: false,
//     // faking API request
//     apiSettings: {
//         loadingDuration : 300,
//         mockResponse    : function(settings) {
//         var response = {
//             first  : 'AJAX Tab One',
//             second : 'AJAX Tab Two',
//             third  : 'AJAX Tab Three'
//         };
//         return response[settings.urlData.tab];
//         }
//     },
//     context : 'parent',
//     auto    : true,
//     path    : '/'
//     })
//     ;
$('.tabular.menu .item').tab();
$('.ui.menu .item')
  .tab({
    history: true,
    historyType: 'state',
    path: '/modules/tab.html'
  })
;