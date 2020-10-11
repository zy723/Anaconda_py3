<template>
	<view class="uni_topbar" :style="style">
		<view class="uni-searchbar">
			<view :class="show ? '' : 'hide'" class="uni-searchbar-form">
				<view v-if="isBack" @tap="goBack" class="goBack">
					<i class="iconfont">&#xe61a;</i>
					<!-- <slot name="back"></slot> -->
				</view>
				<slot name="headerL"></slot>
				<view :style="{ borderRadius: radius + 'rpx' }" class="uni-searchbar-form__box">
					<uni-icons :color="'#999999'" class="icon-search" type="search" size="18" />
					<input
						:placeholder="placeholder"
						:focus="show"
						v-model="searchVal"
						class="search-input"
						type="text"
						placeholder-style="color:#cccccc"
						confirm-type="search"
						@focus="inputFocus"
						@input="tipsearch"
					/>
					<uni-icons
						:color="'#999999'"
						v-if="clearButton === 'always' || (clearButton === 'auto' && searchVal !== '')"
						class="icon-clear"
						type="clear"
						size="24"
						@click="clear"
					/>
				</view>
				<view :style="{ borderRadius: radius + 'rpx' }" class="uni-searchbar-form__text" @click="searchClick">
					<uni-icons color="#999999" class="icon-search" type="search" size="18" />
					<text class="placeholder">{{ placeholder }}</text>
				</view>
			</view>
			<text class="uni-searchbar-form__cancel" @click="cancel">{{ searchtext }}</text>
		</view>
	</view>
</template>

<script>
import uniIcons from '../uni-icons/uni-icons.vue';
export default {
	name: 'UniSearchBar',
	components: {
		uniIcons
	},
	props: {
		placeholder: {
			type: String,
			default: '搜索'
		},
		radius: {
			type: [Number, String],
			default: 10
		},
		clearButton: {
			type: String
		},
		isBack: { type: [Boolean, String], default: true }
	},
	data() {
		return {
			show: false,
			searchVal: '',
			statusBarH: this.statusBar,
			customBarH: this.customBar,
			searchtext: '搜索'
		};
	},
	computed: {
		style() {
			let _style = `height: ${this.customBarH}px;`;
			return _style;
		}
	},
	watch: {
		searchVal() {
			this.$emit('input', {
				value: this.searchVal
			});
		}
	},
	methods: {
		searchClick() {
			this.searchtext = '取消';
			this.searchVal = '';
			this.show = true;
		},
		clear() {
			this.searchVal = '';
			this.searchtext = '搜索';
			this.$emit('clearData')
		},
		inputFocus() {
			//商品清空
			// this.listData = [];
			//展示搜索提示信息
			this.$emit('getInputtips');
		},
		cancel() {
			// this.$emit('cancel', {
			// 	value: this.searchVal
			// });

			this.show = false;
			this.searchVal = '';
			this.searchtext = '搜索';
		},

		tipsearch(e) {
			this.$emit('confirm', e);
		},
		goBack() {
			uni.navigateBack();
		}
	}
};
</script>
<style scoped>
.uni-searchbar {
	display: flex;
}
</style>
<style>
@charset "UTF-8";

.uni-searchbar-form {
	position: relative;
	display: flex;
	padding: 15rpx;
	width: 100%;
	box-sizing: border-box;
}

.uni-searchbar-form__box {
	display: flex;
	/* flex: 1; */
	align-items: center;
	width: 100%;
	height: 64rpx;
	color: #c8c7cc;
	background: #fff;
	border: solid 1px #c8c7cc;
	border-radius: 10rpx;
}

.uni-searchbar-form__box .icon-search {
	color: #c8c7cc;
	line-height: 24px;
	padding: 0rpx 10rpx 0rpx 15rpx;
}

.uni-searchbar-form__box .search-input {
	flex: 1;
	font-size: 28rpx;
	height: 64rpx;
	line-height: 64rpx;
	color: #333;
}

.uni-searchbar-form__box .icon-clear {
	color: #c8c7cc;
	line-height: 20px;
	padding: 0rpx 15rpx 0rpx 10rpx;
}

.uni-searchbar-form__text {
	display: flex;
	/* flex: 1; */
	align-items: center;
	width: 100%;
	height: 64rpx;
	line-height: 64rpx;
	text-align: center;
	color: #c8c7cc;
	background: #fff;
	border: solid 1px #c8c7cc;
	border-radius: 10rpx;
	display: none;
}

.uni-searchbar-form__text .icon-search {
	height: 64rpx;
	line-height: 64rpx;
}

.uni-searchbar-form__text .placeholder {
	display: inline-block;
	font-size: 28rpx;
	color: #ccc;
	margin-left: 10rpx;
}

.uni-searchbar-form__cancel {
	padding-left: 20rpx;
	line-height: 45px;
	color: #333;
	white-space: nowrap;
	padding-right: 20px;
}
.uni-searchbar-form__cancel span {
	line-height: 30px;
}

.uni-searchbar-form.hide .uni-searchbar-form__box {
	display: none;
}

.uni-searchbar-form.hide .uni-searchbar-form__text {
	display: block;
}

.uni-searchbar-form.hide .uni-searchbar-form__cancel {
	display: none;
}
</style>
