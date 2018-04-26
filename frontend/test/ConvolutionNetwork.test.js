import { createLocalVue, mount } from '@vue/test-utils'
import ConvolutionNetwork from '@/components/ConvolutionNetwork'
import BootstrapVue from 'bootstrap-vue'

const factory = (options = {}) => {
  const localVue = createLocalVue()
  localVue.use(BootstrapVue)

  return mount(ConvolutionNetwork, {
    localVue,
    ...options
  })
}

describe('ConvolutionNetwork', () => {
  it('renders a ConvolutionNetwork', () => {
    const wrapper = factory({mocks: {
      $store: {
        state: {
          configuration: {},
        }
    }
    }})
    expect(wrapper)
  })
})