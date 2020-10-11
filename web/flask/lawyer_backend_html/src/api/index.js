import request from '@/common/request.js'
var info='v1_0'
// 登录
// 登录绑定
export const login = data => request.createrApi(`/${info}/authorizations`, data,'POST')

// 首页
// 获取首页列表
export const homeList = data => request.createrApi(`/${info}/new_questions`, data,'GET')
// 获取首页列表-详情
export const homeDetails = data => request.createrApi(`/${info}/question`, data,'GET')
// 获取首页搜索-提示列表
export const tipList = data => request.createrApi(`/${info}/suggestion`, data,'GET')
// 获取首页搜索-查询列表
export const searchList = data => request.createrApi(`/${info}/search`, data,'GET')
// 获取首页搜索-历史列表
export const historyList = data => request.createrApi(`/${info}/search/histories`, data,'GET')
// 获取首页搜索-清空搜索历史
export const clearHistory = data => request.createrApi(`/${info}/search/histories`, data,'DELETE')

// 用户提问
// 获取城市
export const get_linkAddress_api = data => request.addressRequest('/api/address/area',data,'GET')

// 获取省份列表
export const getProvinces = data => request.createrApi(`/${info}/common/provinces`,data,'GET')
// 获取城市列表
export const getCities = data => request.createrApi(`/${info}/common/cities`,data,'GET')
// 获取区域列表
export const getDistricts = data => request.createrApi(`/${info}/common/districts`,data,'GET')
// 普通用户提交问题
export const upQuestion = data => request.fileRequestMore(`/${info}/question`,data,'POST',`${data.value}`,`${data.name}`)

// 律师列表
export const lawyerList = data => request.createrApi(`/${info}/lawyers`,data,'GET')
// 律师详情
export const lawyerDetails = data => request.createrApi(`/${info}/lawyer?id=${data}`,data,'GET')
// 热门律师
export const hotlawyerList = data => request.createrApi(`/${info}/hots_lawyers`,data,'GET')

// 律师关注
export const following = data => request.createrApi(`/${info}/following`,data,'POST')
// 律师取消关注
export const cancelFollowing = data => request.createrApi(`/${info}/following`,data,'DELETE')
// 问题类型
export const getType = data => request.createrApi(`/${info}/common/expertises`,data,'GET')
// export default api