import { createLocalVue, mount } from '@vue/test-utils'
import BlackPaper from '@/components/BlackPaper'
import BootstrapVue from 'bootstrap-vue'

const factory = (options = {}) => {
  const localVue = createLocalVue()
  localVue.use(BootstrapVue)

  return mount(BlackPaper, {
    localVue,
    ...options
  })
}

describe('BlackPaper', () => {
  it('renders a BlackPaper', () => {
    const wrapper = factory()
    expect(wrapper)
  })
})