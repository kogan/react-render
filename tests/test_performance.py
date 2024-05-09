import os
import time
import unittest
from react_render.django import render_component

path_to_component = os.path.abspath(os.path.join(os.path.dirname(__file__), 'components', 'PerfTestComponent.js'))


def median(l):
    half = int(len(l) / 2)
    l.sort()
    if len(l) % 2 == 0:
        return (l[half-1] + l[half]) / 2.0
    else:
        return l[half]


class TestDjangoReactPerformance(unittest.TestCase):
    def test_performance(self):
        print('\n' + ('-' * 80))
        print('react-render performance test')
        print('-' * 80)

        render_component_times = []
        render_watched_component_times = []
        rendered_components = []
        render_b64_prop_times = []
        render_prop_times = []

        iteration_count = 25

        # Generate a set of props with many types of data
        props = {
            'name': 'world',
            'unicode': u'Hello world ',
            'REALLY_LONG_STRING': format(u' '.join([u'War and Peace and ' for i in range(100000)])),
            'wave emoji': u'👋',
            'integer': 123,
            'float': 123.456,
            'array': [1, 2, 3, 4, 5],
            'object': {
                'key': 'value',
                'key2': 'value2',
            }
        }

        for i in range(iteration_count):
            start = time.time()
            rendered_components.append(
                render_component(path_to_component, props=props, to_static_markup=True)
            )
            end = time.time()
            render_component_times.append(end - start)

        for i in range(iteration_count):
            start = time.time()
            rendered_components.append(
                render_component(path_to_component, props=props, to_static_markup=True)
            )
            end = time.time()
            render_watched_component_times.append(end - start)

        for component in rendered_components:
            start = time.time()
            component.render_props_b64()
            end = time.time()
            render_b64_prop_times.append(end - start)

        for component in rendered_components:
            start = time.time()
            component.render_props()
            end = time.time()
            render_prop_times.append(end - start)

        for component in rendered_components:
            self.assertEqual(str(component), '<span>Hello world</span>')

        print('Total time taken to render a component {iteration_count} times: {value}'.format(
            iteration_count=iteration_count,
            value=sum(render_component_times)
        ))
        print('Times: {value}'.format(value=render_component_times))
        print('Max: {value}'.format(value=max(render_component_times)))
        print('Min: {value}'.format(value=min(render_component_times)))
        print('Mean: {value}'.format(value=sum(render_component_times) / len(render_component_times)))
        print('Median: {value}'.format(value=median(render_component_times)))

        print('\nTotal time taken to render a watched component {iteration_count} times: {value}'.format(
            iteration_count=iteration_count,
            value=sum(render_watched_component_times)
        ))
        print('Times: {value}'.format(value=render_watched_component_times))
        print('Max: {value}'.format(value=max(render_watched_component_times)))
        print('Min: {value}'.format(value=min(render_watched_component_times)))
        print('Mean: {value}'.format(value=sum(render_watched_component_times) / len(render_watched_component_times)))
        print('Median: {value}'.format(value=median(render_watched_component_times)))

        print('\nTotal time taken to render props {iteration_count} times: {value}'.format(
            iteration_count=iteration_count,
            value=sum(render_prop_times)
        ))
        print('Times: {value}'.format(value=render_prop_times))
        print('Max: {value}'.format(value=max(render_prop_times)))
        print('Min: {value}'.format(value=min(render_prop_times)))
        print('Mean: {value}'.format(value=sum(render_prop_times) / len(render_prop_times)))
        print('Median: {value}'.format(value=median(render_prop_times)))

        print('\nTotal time taken to render props b64 {iteration_count} times: {value}'.format(
            iteration_count=iteration_count,
            value=sum(render_b64_prop_times)
        ))
        print('Times: {value}'.format(value=render_b64_prop_times))
        print('Max: {value}'.format(value=max(render_b64_prop_times)))
        print('Min: {value}'.format(value=min(render_b64_prop_times)))
        print('Mean: {value}'.format(value=sum(render_b64_prop_times) / len(render_b64_prop_times)))
        print('Median: {value}'.format(value=median(render_b64_prop_times)))
