// 参数： url:请求地址  param：请求参数  method：请求方式 callBack：回调函数
const request = {}
const BaseUrl = ' http://119.23.52.42:5000'
// const BaseUrl = ' http://127.0.0.1:5000'

var token = uni.getStorageSync('access_token');

// token = uni.getStorageSync('access_token');
request.addressRequest = (paramete, data, method) => {
	let BASE_API = "http://admin.farmereasy.com";
	return new Promise((resolve, reject) => {
		uni.request({
			url: `${BASE_API}${paramete}`,
			data: data,
			method: method,
			success: (res) => {
				resolve(res);
			},
			fail: (res) => {
				resolve(0);
			}
		})
	});
}
// 单个文件上传
request.fileRequest = (url, data, method) => {
	return new Promise((resolve, reject) => {
		uni.uploadFile({
			url: BaseUrl + url,
			filePath: data,
			name: 'photo',
			method: method,
			header: {
				'Authorization': `Bearer ${token}`,
			},
			success(uploadFileRes) {
				resolve(uploadFileRes);
			}
		});
	});
}
// 多个文件上传
request.fileRequestMore = (url, data, method, value, name) => {
	return new Promise((resolve, reject) => {
		wx.uploadFile({
			url: BaseUrl + url,
			filePath: value,
			name: name,
			method: method,
			formData: JSON.parse(data.formData),
			header: {
				'Authorization': `Bearer ${token}`,
			},
			success(uploadFileRes) {
				resolve(uploadFileRes);
			}
		});
	});
}
request.createrApi = (url, data, method) => {
	// const BaseUrl = 'https://mock.boxuegu.com/mock/653'

	let state = token === "" ? true : false

	if (url === '/v1_0/authorizations' || url === '/v1_0/new_client' || url === '/v1_0/sms_code/' + data) {
		state = false
	}
	if (state) {
		uni.showToast({
			icon: 'none',
			title: '登录失效，请重新登录！'
		});
		uni.navigateTo({
			url: '/pages/user/login'
		})
	}

	let header = {
		// 'Accept': 'application/json',
		'Access-Control-Allow-Origin': '*'
	}
	if (url == '/v1_0/question') {
		header = {
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
		}

	}
	if (url === '/v1_0/photo') {
		header = {
			'Content-Type': 'multipart/form-data',
			'Access-Control-Allow-Methods': 'POST',
		}

	}
	if (token) {
		header = { ...header,
			'Authorization': `Bearer ${token}`,
		}
	}
	return new Promise((resolve, reject) => {
		uni.request({
			url: BaseUrl + url,
			data: data,
			header: header,
			method: method,
			success: (res) => {
				resolve(res)
				// if (res.data.code == 0 ){
				// 	resolve(res)
				// }else{
				// 	reject(res)
				// }
			},
			fail: (err) => {
				resolve(err)
			}
		});
	})
	// return requestRes
}
export default request
