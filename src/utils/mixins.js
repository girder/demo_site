import Vue from 'vue';
import { mapGetters } from 'vuex';
import { AccessType } from '@/constants';

/**
 * This mixin exposes helper methods for components that need to check that the current user has
 * a certain access level on a given resource.
 */
export const accessLevelChecker = {
  methods: {
    hasWriteAccess: resource => resource._accessLevel >= AccessType.WRITE,
    hasAdminAccess: resource => resource._accessLevel >= AccessType.ADMIN,
  },
};

/**
 * This mixin should be used on any container component whose data needs to be
 * fetched on initialization and also on user login/logout. Components using this mixin
 * must implement a ``fetch`` method.
 */
export const fetchingContainer = {
  computed: mapGetters('auth', ['isLoggedIn']),
  // Use mounted hook instead of created so that $refs is available in fetch()
  mounted() {
    this.fetch();
  },
  watch: {
    isLoggedIn() {
      this.fetch();
    },
  },
};

/**
 * Router components that wrap container components that should fetch data on route change
 * should mix this in, and add a "wrapped" ref to their container component.
 */
export const fetchingRoute = {
  watch: {
    $route() {
      // This watch callback gets triggered before the data gets flowed down to child components,
      // so we need to wait until the next tick to fetch.
      Vue.nextTick().then(() => {
        this.$refs.wrapped.fetch();
      });
    },
  },
};

/**
 * A simple mixin for checking if browser is a mobile browser.
 * https://stackoverflow.com/questions/11381673/detecting-a-mobile-browser
 */
export const mobileChecker = {
  computed: {
    isMobile() {
      let check = false;
      // eslint-disable-next-line no-useless-escape
      const mobileAgentRegex = /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i;
      // eslint-disable-next-line no-useless-escape
      const first4 = /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i;
      const userAgent = navigator.userAgent || navigator.vendor || window.opera;
      if (mobileAgentRegex.test(userAgent)) {
        check = true;
      } else if (first4.test(userAgent.substr(0, 4))) {
        check = true;
      }
      return check;
    },
  },
};

/**
 * Containers that must fetch lists of data in pages should use this mixin. The container is
 * responsible for calling "transformDataPage" on the returned list, which will automatically
 * update the "hasNextPage" data field and remove the last document from the list if necessary.
 * The original Array passed to "transformDataPage" is not modified; a shallow copy is returned
 * in the case when it requires modification.
 */
export const pagingContainer = {
  props: {
    pageSize: {
      default: 30,
      type: Number,
    },
  },
  data: () => ({
    pageOffset: 0,
    hasNextPage: false,
  }),
  computed: {
    hasPrevPage() {
      return this.pageOffset > 0;
    },
    currentPage() {
      return this.pageOffset / this.pageSize;
    },
    pagingParams() {
      return {
        limit: this.pageSize + 1,
        offset: this.pageOffset,
      };
    },
  },
  methods: {
    fetchNextPage() {
      this.pageOffset += this.pageSize;
      return this.fetch();
    },
    fetchPrevPage() {
      this.pageOffset = Math.max(0, this.pageOffset - this.pageSize);
      return this.fetch();
    },
    fetchPage(n) {
      this.pageOffset = this.pageSize * n;
      return this.fetch();
    },
    transformDataPage(list) {
      this.hasNextPage = list.length > this.pageSize;
      if (this.hasNextPage) {
        return list.slice(0, -1);
      }
      return list;
    },
  },
};

/**
 * Any view component that needs to display human-readable data sizes should use this.
 */
export const sizeFormatter = {
  methods: {
    formatDataSize(size) {
      if (size < 1024) {
        return `${size} B`;
      }

      let i;
      for (i = 0; size >= 1024; i += 1) {
        size /= 1024;
      }

      return `${size.toFixed(2)}  ${['B', 'KB', 'MB', 'GB', 'TB'][Math.min(i, 4)]}`;
    },
  },
};

/**
 * Container components that need to expose slots from their child components should use this.
 * It exposes a special property "view-slots" that parents can set to indicate which of the
 * view slots are being overridden. This should be an Array of strings for named slots, or
 * for the default slot, use ``null`` instead of a string.
 */
export const viewSlotWrapper = {
  props: {
    viewSlots: {
      default: () => [],
      type: Array,
    },
  },
};
