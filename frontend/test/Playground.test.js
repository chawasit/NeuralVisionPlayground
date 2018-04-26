import { createLocalVue, mount } from '@vue/test-utils'
import Playground from '@/components/Playground'
import BootstrapVue from 'bootstrap-vue'

const factory = (options = {}) => {
  const localVue = createLocalVue()
  localVue.use(BootstrapVue)

  return mount(Playground, {
    localVue,
    ...options
  })
}

describe('Playground', () => {
  it('renders a Playground', () => {
    const wrapper = factory({mocks: {
      $store: {
        state: {
          configuration: {},
          train: { epoch: 0, accuracy: [] },
          result: null,
        }
    }
    }})
    expect(wrapper).toBeDefined()
  })
})