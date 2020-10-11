import request from '@/common/request.js'
var info='v1_0'
// 登录
export const login = data => request.createrApi(`/${info}/authorizations`, data,'POST')
// 登录绑定
export const token = data => request.createrApi(`/${info}/authorizations`, data,'PUT')
// 注册
export const reg = data => request.createrApi(`/${info}/new_client`, data,'POST')
// 获取二维码
export const code = data => request.createrApi(`/${info}/sms_code/${data}`, data,'GET')
