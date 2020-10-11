<template>
	<view class="popup-layout-wrap " :class="popuplayoutClass">
		<view class="popup-layout-content" :class="popupContentClass" :style="[{ height: height }]">
			<view class="link-address-wrap">
				<view class="link-adress-content">
					<view class="head-wrap">
						<text class="cancel" @click="btn_cancel">取消</text>
						<text class="confirm" @click="btn_confirm">确认</text>
					</view>
					<!-- <view class="head-selected">
						<text class="selected-txt">已选择:{{ selected_address }}</text>
					</view> -->
					<view class="operation-wrap">
						<view class="operation-container">
							<view class="operation-content" v-for="(base_items, base_index) of linkAddress_area">
								<scroll-view scroll-y="true" class="province" show-scrollbar="false">
									<view
										@click="choosefun(base_items,base_items.clickfun, items.id)"
										v-model="items.id"
										v-for="(items, index) of base_items.info"
										:class="[index == base_items.current ? 'province-txt-click' : 'province-txt']"
									>
										{{ items.name }}
										<!-- <view class="pic" v-show="index === base_items.current"><image src="/../../static/image/yes.png"></image></view> -->
									</view>
								</scroll-view>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		<view v-if="maskShow" class="popup-layout-mask" @tap="close(maskClick)"></view>
	</view>
</template>

<script>
import linkAddress_p from './get_linkAddress_p.js';
import {getProvinces} from '@/api/index.js';
export default {
	data() {
		return {
			newActive: '',
			newTransition: true,
			//省0市1区2
			linkAddress_area: [
				{
					current: null,
					info: [],
					clickfun: 'province_txt_click'
				},
				{
					current: null,
					info: [],
					clickfun: 'city_txt_click'
				},
				{
					current: null,
					info: [],
					clickfun: 'district_txt_click'
				}
			],
			/*请求提交的*/
			submission: {
				province: '', //省
				city: '', //市
				county: '', //区
				town: '' //镇
			},
			/*用户选择的地址*/
			user_address: {
				province: '', //省
				city: '', //市
				district: '' //区
			},
			selected_address: '',
			byID:'1'
		};
	},
	props: {
		/*底部弹窗的属性*/
		active: {
			type: Boolean,
			default: false
		},
		height: {
			type: [String],
			default: '100%'
		},
		//遮盖层显示
		maskShow: {
			type: Boolean,
			default: true
		},
		//遮盖层点击
		maskClick: {
			type: Boolean,
			default: true
		},
		//回掉
		callback: {
			type: Function,
			default: function() {}
		}
	},
	computed: {
		popuplayoutClass: function() {
			let _class = '';
			if (this.newActive) {
				_class += 'popup-layout-active';
			}
			_class += ' popup-layout-bottom';
			return _class;
		},
		popupContentClass: function() {
			let _class = '';
			if (this.newTransition && this.transition !== 'none') {
				_class += 'popup-layout-transition-slider';
			}
			return _class;
		}
	},
	methods: {
		childMethod() {
			console.log('childMethod do...');
		},
		//显示弹窗
		show: function() {
			// getProvinces()
			// .then(res => {
			// 	console.log(666,res)
			// })
			// .catch(err => {});
			//提交的数据置为空
			(this.submission = {
				province: '',
				city: '',
				county: '',
				town: ''
			}),
				//请求市数据
				linkAddress_p.get_linkAddress(this, 'province', this.submission, revert => {
					this.submission.province = '1';
				});
			this.newActive = true;
			let _this = this;
			setTimeout(function() {
				_this.newTransition = false;
			}, 50);
			
			
		},

		//关闭弹窗
		close: function(v) {
			let close = v || true;
			if (close) {
				this.newTransition = true;
				let _this = this;
				setTimeout(function() {
					_this.newActive = false;
				}, 300);
			}
		},
		//选择点击事件
		choosefun(baseitems,targetfun, targetid) {
			console.log(targetid)
			this[targetfun](targetid);
		},
		//省点击选择
		province_txt_click(target) {
			//区数据置为空
			this.linkAddress_area[2].info = [];
			//市、区的选择计数置为null
			this.linkAddress_area[1].current = null;
			this.linkAddress_area[2].current = null;
			let provinceName;
			let provinceId;
			//得到点击的数据，改变样式
			for (let i = 0; i < this.linkAddress_area[0].info.length; i++) {
				if (this.linkAddress_area[0].info[i].id === target) {
					this.linkAddress_area[0].current = i;
					provinceName = this.linkAddress_area[0].info[i].name;
					provinceId = this.linkAddress_area[0].info[i].id;
					break;
				}
			}

			//用户选择
			this.user_address = {
				province:{
					id:provinceId,
					name: provinceName,
				},
				city:{
					id:'',
					name: '',
				},
				district:{
					id:'',
					name: '',
				}
			};
			//请求提交的数据先置为空
			this.submission = {
				province: '',
				city: '',
				county: '',
				town: ''
			};
			//再赋值

			this.submission.province = target;
			this.selected_address = this.user_address.province;
			//请求市数据
			linkAddress_p.get_linkAddress(this, 'city', this.submission, revert => {});
		},

		//市点击选择
		city_txt_click(target) {
			//区的选择计数置为null
			this.linkAddress_area[2].current = null;
			let cityName;
			let cityId;
			//得到点击的数据，改变样式
			for (let i = 0; i < this.linkAddress_area[1].info.length; i++) {
				if (this.linkAddress_area[1].info[i].id === target) {
					this.linkAddress_area[1].current = i;
					cityName = this.linkAddress_area[1].info[i].name;
					cityId = this.linkAddress_area[1].info[i].id;
					break;
				}
			}
			//得到市
			this.user_address.city.name = cityName;
			this.user_address.city.id = cityId;
			//把区的信息置为空
			this.user_address.district = {};

			this.submission.city = target;

			this.selected_address = this.user_address.province.name + '-' + this.user_address.city.name;
			//请求区数据
			linkAddress_p.get_linkAddress(this, 'district', this.submission, revert => {});
		},
		//区点击选择
		district_txt_click(target) {
			let districtName;
			let districtId;
			//得到点击的数据，改变样式
			for (let i = 0; i < this.linkAddress_area[2].info.length; i++) {
				if (this.linkAddress_area[2].info[i].id === target) {
					// this.district_current = i;
					this.linkAddress_area[2].current = i;
					districtName = this.linkAddress_area[2].info[i].name;
					districtId = this.linkAddress_area[2].info[i].id;
					break;
				}
			}
			//得到区信息
			this.user_address.district.name = districtName;
			this.user_address.district.id = districtId;
			this.selected_address = this.user_address.province.name + '-' + this.user_address.city.name + '-' + this.user_address.district.name;
		},

		//取消按钮
		btn_cancel: function() {
			this.close();

			//全部置为空
			this.submission = {
				province: '',
				city: '',
				county: '',
				town: ''
			};
			this.linkAddress_area[1].info = [];
			this.linkAddress_area[2].info = [];
			this.linkAddress_area[0].current = null;
			this.linkAddress_area[1].current = null;
			this.linkAddress_area[2].current = null;
			this.selected_address = '';
		},
		//确定按钮
		btn_confirm: function() {
			this.close();
			//可以使用vuex传值
			this.$store.commit('commit_address', this.user_address);
			this.$emit('confirmCallback',this.byID);
		}
	}
};
</script>

<style>
.link-address-wrap .link-adress-content .operation-wrap .operation-container {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
}
.link-address-wrap .link-adress-content .operation-wrap .operation-container .operation-content {
	display: flex;
	flex-direction: column;
	width: 33.333%;
}
</style>
