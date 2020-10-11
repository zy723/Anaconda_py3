<template>
	<view style="width: 100%;">
		<view class="example-box example-body">
			<view class="uni-padding-wrap uni-common-mt uni-form">
				<form @submit="handleSub">
					<view class="uni-form-item uni-column textInput">
						<input class="uni-input" name="title" @input="conInput(1, $event)" placeholder="请在此输入您的法律问题，祝您的问题早日得到解决..." />
						<view class="text_right" v-if="formItem.title.length > 0">
							<view class="em" style="color:red">{{ inputVal }}</view>
							/
							<view class="span">60</view>
						</view>
					</view>
					<view class="text">
						<textarea maxlength="300" name="content" rows="2" placeholder="请再次补充您问题的详情" placeholder-class="plac" @input="conInput(2, $event)"></textarea>
						<view class="text_right" v-if="formItem.content.length > 0">
							<view class="em" style="color:red">{{ textVal }}</view>
							/
							<view class="span">300</view>
						</view>
					</view>
					<view class="uni-form-item uni-column uni-card__header">
						<view>事发城市：{{ address }}</view>
						<view class="uni-card__header-extra-text"><span @tap="popup_bottom()" class="tabAddress">[切换城市]</span></view>

						<linkAddress ref="linkAddress" :height="height" @confirmCallback="confirmCallback()"></linkAddress>
					</view>
					<view class="uni-form-item uni-column uni-card__header">
						<view class="uni-card__header-title-text">分类：{{ classData.expertise_name }}</view>
						<view class="uni-card__header-extra-text">
							<span @tap="togglePopup()" class="classTip"><i class="iconfont">&#xe613;</i></span>
						</view>
						<uni-popup ref="popup" :height="height" @classCallback="classCallback()" :bottomData="bottomData"></uni-popup>
					</view>
					<uniUpload
						ref="upload"
						:imageList="imageList"
						:imageLength="imageLength"
						:sourceTypeIndex="sourceTypeIndex"
						:sizeTypeIndex="sizeTypeIndex"
						@chooseImage="chooseImage"
						@previewImage="previewImage"
						@deleteImage="deleteImage"
					></uniUpload>
					<view class="table-btn-view bttomBox"><button class="save-btn" type="primary" form-type="submit">提交问题</button></view>
					<uni-popups ref="popups" :type="type" @change="change" class="popupBox">
						<view class="tipBox">
							<div class="successBox" v-if="successShow"></div>
							<div class="errorBox" v-else></div>
							<p>{{ successText }}</p>
						</view>
					</uni-popups>
				</form>
			</view>
		</view>
	</view>
</template>

<script>
import linkAddress from '../../../components/address/address.vue';
import uniPopup from '@/components/uni-popup/uni-popup.vue';
import uniPopups from '@/components/uni-popup/uni-popups.vue';
import uniUpload from '@/components/uni-upimage/index.vue';
import graceChecker from '@/common/graceChecker.js';
import baseMixin from '@/common/baseMixin.js';
import baseApi from '@/api/baseData/baseData.js';
import { upQuestion,getType } from '@/api/index.js';
var sourceType = [
	['camera'], //拍照
	['album'], //相册
	['camera', 'album'] //拍照或相册
];
var sizeType = [
	['compressed'], //压缩
	['original'], //原图
	['compressed', 'original'] //压缩或原图
];
export default {
	mixins: [baseMixin],
	components: {
		linkAddress,
		uniPopup,
		uniUpload,
		uniPopups
	},
	data() {
		return {
			height: '100%',
			address: '北京-市辖区-东城区',
			classData: {},
			imageList: [], //保存图片路径集合
			imageLength: 3, //限制图片张数
			sourceTypeIndex: 2, //添加方式限制
			sizeTypeIndex: 2, //图片尺寸限制
			errorTip: '',
			formItem: {
				title: '',
				content: '',
				city_id: '110100'
			},

			textVal: 0,
			inputVal: 0,
			remnant: 0,
			type: '',
			successShow: false,
			successText: '支付成功',
			bottomData: []
		};
	},
	onLoad() {
		this.GetType()
	},
	methods: {
		// 输入字数限制
		conInput(num, e) {
			console.log(num);
			if (num === 1) {
				this.inputVal = e.detail.value.length;
				if (this.inputVal == 60) {
					uni.showToast({
						icon: 'none',
						title: '最多只能輸入60個字'
					});
				}
			}
			if (num === 2) {
				this.textVal = e.detail.value.length;
				if (this.textVal == 300) {
					uni.showToast({
						icon: 'none',
						title: '最多只能輸入300個字'
					});
				}
			}
		},
		//点击弹出弹窗
		popup_bottom: function() {
			this.height = '550rpx';
			//显示
			this.show_popup();
		},
		//显示弹窗
		show_popup: function() {
			this.$refs.linkAddress.show();
		},
		//回掉
		confirmCallback: function() {
			let ads = this.$store.state.user_address;
			this.address = ads.province.name + '-' + ads.city.name + '-' + ads.district.name;
			this.formItem.city_id = String(ads.province.id) + String(ads.city.id) + String(ads.district.id);
		},
		//回掉
		classCallback: function() {
			let ads = this.$store.state.classData;
			this.classData = ads;
		},
		change: function(e) {
			console.log(e.show);
		},
		togglePopup: function(type, open) {
			this.height = '550rpx';
			this.$refs.popup.show();
		},
		//选择图片
		chooseImage: async function() {
			uni.chooseImage({
				sourceType: sourceType[this.sourceTypeIndex],
				// #ifdef MP-WEIXIN
				sizeType: sizeType[this.sizeTypeIndex],
				// #endif
				count: this.imageLength - this.imageList.length,
				success: res => {
					this.imageList = this.imageList.concat(res.tempFilePaths);
					var imgFiles = res.tempFilePaths[0];
					console.log(imgFiles);
				}
			});
		},
		//预览图片
		previewImage: function(e) {
			var current = e.target.dataset.src;
			uni.previewImage({
				current: current,
				urls: this.imageList
			});
		},
		//删除图片
		deleteImage: function(e) {
			var index = e.target.dataset.index;
			var that = this;
			var images = that.imageList;
			images.splice(index, 1);
			that.imageList = images;
		},
		// 表单提交
		handleSub: function(e) {
			var that = this;
			var formData = e.detail.value;
			formData.title = e.detail.value.title;
			formData.content = e.detail.value.content;
			formData.expertise_id = this.classData.expertise_id;
			formData.city_id = this.formItem.city_id;
			this.type = 'center';

			//定义表单规则
			var rule = [
				{ name: 'title', checkType: 'notnull', checkRule: '', errorMsg: '标题不能为空' },
				{ name: 'content', checkType: 'notnull', checkRule: '', errorMsg: '详情不能为空' }
			];

			//进行表单检查
			var checkRes = graceChecker.check(formData, rule);
			if (checkRes) {
				var token = uni.getStorageSync('access_token');
				for (var i = 0; i < that.imageList.length; i++) {
					upQuestion({
						formData: JSON.stringify(formData),
						value: that.imageList[i],
						name: 'p' + i
					}).then(res => {
						console.log(res);
						if (res.statusCode === 401) {
							uni.navigateTo({
								url: '/pages/user/login'
							});
						} else {
							this.successShow = true;
							uni.showToast({ title: '验证通过!', icon: 'none' });
							setTimeout(function() {
								this.$refs.popups.open();
							}, 500);
						}
					});
					// wx.uploadFile({
					// 	url: 'http://119.23.52.42:5000/v1_0/question',
					// 	filePath: that.imageList[i],
					// 	name: 'p' + i,
					// 	formData: {
					// 		title: e.detail.value.title,
					// 		content: e.detail.value.content,
					// 		expertise_id: that.classData.id,
					// 		city_id: that.formItem.city_id
					// 	},
					// 	header: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST','Authorization': `Bearer ${token}`, },
					// 	success: res => {
					// 		if (res.data.code == 200) {
					// 			console.log('上传成功');
					// 		}
					// 	}
					// });
				}
				
				
			} else {
				uni.showToast({ title: graceChecker.error, icon: 'none' });
			}
		},
		// 问题类型
		GetType(){
			getType().then(res=>{
				console.log(res)
				if(res.statusCode===200){
					this.bottomData=res.data.data_list
					this.classData.expertise_id=this.bottomData[0].expertise_id
					this.classData.expertise_name=this.bottomData[0].expertise_name
				}
				
			}).catch(err=>{})
		}
	}
};
</script>

<style>
 .order-btn {
	display: block;
	width: 100%;
	height: 90upx;
	line-height: 90upx;
	text-align: center;
	color: white;
	font-size: 32upx;
	background-color: #e11c1c;
	border-radius: 20upx;
	margin: 0upx auto;
}
.input_text {
	width: 100%;
	height: 100upx;
	margin: 20upx auto;
	background-color: #fff;
	border-radius: 20upx;
}
.input_text input {
	border: none;
	border-radius: 16upx;
	padding: 20upx;
}
::-webkit-input-placeholder {
	color: #ccc;
	font-size: 14px;
}
.text {
	width: 100%;
	height: 300upx;
	margin: 10upx auto;
	/* overflow-y: scroll; */
	position: relative;
	padding: 0 0 30px;
}
.text textarea {
	width: 100%;
	height: 300upx;
	background-color: #fff;
	border-radius: 20upx;
	border: none;
	padding: 20upx;
	padding: 0;
}
.text .text_right {
	position: absolute;
	right: 50upx;
	margin-top: -60upx;
	font-size: 14px;
	display: flex;
	bottom: 0;
}
.textInput {
	position: relative;
}
.uni-form .textInput .uni-input {
	padding-right: 40px;
}
.textInput .text_right {
	position: absolute;
	right: 10upx;
	margin-top: 15upx;
	font-size: 14px;
	display: flex;
}
</style>
