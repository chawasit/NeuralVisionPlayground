import { createLocalVue, mount } from '@vue/test-utils'
import Navbar from '@/components/Navbar'
import BootstrapVue from 'bootstrap-vue'

const factory = (options = {}) => {
  const localVue = createLocalVue()
  localVue.use(BootstrapVue)

  return mount(Navbar, {
    localVue,
    ...options
  })
}

describe('Navbar', () => {
  it('renders a navbar', () => {
    const wrapper = factory()
    expect(wrapper.find('#band-title').text()).toEqual("Neural Vision Playground")
  })
})