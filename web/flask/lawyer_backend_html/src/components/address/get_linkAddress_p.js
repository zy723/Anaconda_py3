import {get_linkAddress_api,getProvinces,getCities,getDistricts} from '../../api/index.js';

export default {
	/*
	*_this:全局this
	* data:数据(参数)
	* callback:回掉
	*/
	get_linkAddress: function(_this,tag,data,callback) {
		// console.log(_this.user_address.province.id)
		//请求
		// get_linkAddress_api(data).then((res) => {
		// 	let revert=res.data.data;
		// 	// console.log(revert)
		// 	if(res.data.code==1){
		// 		if(tag==="province"){	
		// 			console.log("province")
		// 			_this.linkAddress_area[0].info=revert;
		// 			callback(true);//回掉
		// 		}
		// 		if(tag==="city"){
		// 			console.log("city")
		// 			_this.linkAddress_area[1].info=revert;
		// 			console.log(revert)
		// 			callback(true);//回掉
		// 		}
		// 		if(tag==="district"){
		// 			console.log("district")
		// 			_this.linkAddress_area[2].info=revert;
		// 			console.log(revert)
		// 			callback(true);//回掉
		// 		}
		// 	}
		// });
		if(tag==="province"){
			// console.log("province")
			// _this.linkAddress_area[0].info=revert;
			let data=[]
			let obj={}
			getProvinces().then(res=>{
				// console.log(res.data)
				let resData=res.data
				for(var i=0;i<resData.length;i++){
					obj={
						id:resData[i].province_id,
						name:resData[i].province_name
					}
					data.push(obj)
				}
				_this.linkAddress_area[0].info=data
			}).catch(err=>{
				
			})
			callback(true);//回掉
		}
		if(tag==="city"){
			// console.log("city")
			let data=[]
			let obj={}
			getCities({'pid':_this.user_address.province.id}).then(res=>{
				let resData=res.data
				for(var i=0;i<resData.length;i++){
					obj={
						id:resData[i].city_id,
						name:resData[i].city_name
					}
					data.push(obj)
				}
				_this.linkAddress_area[1].info=data
			}).catch(err=>{
				
			})
			callback(true);//回掉
		}
		if(tag==="district"){
			// console.log("district")
			let data=[]
			let obj={}
			getDistricts({'pid':_this.user_address.city.id}).then(res=>{
				let resData=res.data
				for(var i=0;i<resData.length;i++){
					obj={
						id:resData[i].district_id,
						name:resData[i].district_name
					}
					data.push(obj)
				}
				_this.linkAddress_area[2].info=data
			}).catch(err=>{
				
			})
			callback(true);//回掉
		}
	}
}
