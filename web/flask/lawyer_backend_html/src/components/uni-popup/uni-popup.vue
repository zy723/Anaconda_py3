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
						<text class="selected-txt">已选择:{{ classData }}</text>
					</view> -->
					<view class="operation-wrap">
						<view class="operation-container">
							<scroll-view scroll-y="true" class="province" show-scrollbar="false">
								<view
									class="uni-share-content-text"
									v-for="(item, index) in bottomData"
									:key="index"
									:class="current == index ? 'province-txt-click' : 'province-txt'"
									@click="province_txt_click(item, index)"
								>
									{{ item.expertise_name }}
								</view>
							</scroll-view>
						</view>
					</view>
				</view>
			</view>
		</view>
		<view v-if="maskShow" class="popup-layout-mask" @tap="close(maskClick)"></view>
	</view>
</template>

<script>
// import linkAddress_p from './get_linkAddress_p.js';
export default {
	data() {
		return {
			newActive: '',
			newTransition: true,
			classData: '',
			current: 0,
			byID:'2'
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
		bottomData: {
			type: Array
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
		choosefun(targetfun, targetid) {
			this[targetfun](targetid);
		},
		//省点击选择
		province_txt_click(target, index) {
			this.current = index;
			this.classData = target;
		},
		//取消按钮
		btn_cancel: function() {
			this.close();
			this.classData = '';
		},
		//确定按钮
		btn_confirm: function() {
			this.close();
			console.log(this.classData);
			//可以使用vuex传值
			this.$store.commit('commit_xingshi', this.classData);
			this.$emit('classCallback', this.byID);
		}
	}
};
</script>

<style></style>
