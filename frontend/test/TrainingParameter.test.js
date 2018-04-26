import { createLocalVue, mount } from '@vue/test-utils'
import TrainingParameter from '@/components/TrainingParameter'
import BootstrapVue from 'bootstrap-vue'

const factory = (options = {}) => {
  const localVue = createLocalVue()
  localVue.use(BootstrapVue)

  return mount(TrainingParameter, {
    localVue,
    ...options
  })
}

describe('TrainingParameter', () => {
  it('renders a TrainingParameter', () => {
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