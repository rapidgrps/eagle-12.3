# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

from eagle import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    code = fields.Selection(selection_add=[('mrp_operation', 'Manufacturing Operation')])
    count_mo_todo = fields.Integer(string="Number of Manufacturing Orders to Process",
        compute='_get_mo_count')
    count_mo_waiting = fields.Integer(string="Number of Manufacturing Orders Waiting",
        compute='_get_mo_count')
    count_mo_late = fields.Integer(string="Number of Manufacturing Orders Late",
        compute='_get_mo_count')

    def _get_mo_count(self):
        mrp_picking_types = self.filtered(lambda picking: picking.code == 'mrp_operation')
        if not mrp_picking_types:
            return
        domains = {
            'count_mo_waiting': [('availability', '=', 'waiting')],
            'count_mo_todo': [('state', 'in', ('confirmed', 'planned', 'progress'))],
            'count_mo_late': [('date_planned_start', '<', fields.Date.today()), ('state', '=', 'confirmed')],
        }
        for field in domains:
            data = self.env['mrp.production'].read_group(domains[field] +
                [('state', 'not in', ('done', 'cancel')), ('picking_type_id', 'in', self.ids)],
                ['picking_type_id'], ['picking_type_id'])
            count = {x['picking_type_id'] and x['picking_type_id'][0]: x['picking_type_id_count'] for x in data}
            for record in mrp_picking_types:
                record[field] = count.get(record.id, 0)

    def get_mrp_stock_picking_action_picking_type(self):
        return self._get_action('mrp.mrp_production_action_picking_deshboard')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _less_quantities_than_expected_add_documents(self, moves, documents):
        documents = super(StockPicking, self)._less_quantities_than_expected_add_documents(moves, documents)

        def _keys_in_sorted(move):
            """ sort by picking and the responsible for the product the
            move.
            """
            return (move.raw_material_production_id.id, move.product_id.responsible_id.id)

        def _keys_in_groupby(move):
            """ group by picking and the responsible for the product the
            move.
            """
            return (move.raw_material_production_id, move.product_id.responsible_id)

        production_documents = self._log_activity_get_documents(moves, 'move_dest_ids', 'DOWN', _keys_in_sorted, _keys_in_groupby)
        return {**documents, **production_documents}
