let url_config = ""

if(process.env.NODE_ENV === 'development'){
    // 开发环境
    url_config = 'https://mock.boxuegu.com/mock/653'
}else{
    // 生产环境
    url_config = 'https://mock.boxuegu.com/mock/653'
}

export default url_config