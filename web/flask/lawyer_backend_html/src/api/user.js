import request from '@/common/request.js'
var info='v1_0'

// 用户信息
export const userInfo = data => request.createrApi(`/${info}/user_info_s`, data,'GET')
// 普通用户个人中心详细信息
export const userDetails = data => request.createrApi(`/${info}/user_info_d`, data,'GET')
export const userRevamp = data => request.createrApi(`/${info}/user_info_d`, data,'PUT')
export const upPhoto = data => request.fileRequest(`/${info}/photo`, data,'POST')