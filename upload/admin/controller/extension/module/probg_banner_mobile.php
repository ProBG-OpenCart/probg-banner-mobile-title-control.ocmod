<?php
class ControllerExtensionModuleProbgBannerMobile extends Controller {
	public function index() {
		$this->load->language('extension/module/probg_banner_mobile');
		$this->document->setTitle($this->language->get('heading_title'));

		$data['breadcrumbs'] = array();
		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true)
		);
		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_extension'),
			'href' => $this->url->link('marketplace/extension', 'user_token=' . $this->session->data['user_token'] . '&type=module', true)
		);
		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('heading_title'),
			'href' => $this->url->link('extension/module/probg_banner_mobile', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['banner_url'] = $this->url->link('design/banner', 'user_token=' . $this->session->data['user_token'], true);
		$data['modules_url'] = $this->url->link('marketplace/extension', 'user_token=' . $this->session->data['user_token'] . '&type=module', true);

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->response->setOutput($this->load->view('extension/module/probg_banner_mobile', $data));
	}

	public function install() {
		if (!$this->columnExists('banner_image', 'mobile_image')) {
			$this->db->query("ALTER TABLE `" . DB_PREFIX . "banner_image` ADD `mobile_image` VARCHAR(255) NOT NULL DEFAULT '' AFTER `image`");
		}

		if (!$this->columnExists('banner_image', 'hide_title')) {
			$this->db->query("ALTER TABLE `" . DB_PREFIX . "banner_image` ADD `hide_title` TINYINT(1) NOT NULL DEFAULT '0' AFTER `mobile_image`");
		}
	}

	public function uninstall() {
		// Intentionally keep the added columns and data. They are harmless without the OCMOD
		// and preserving them prevents data loss when the extension is reinstalled or upgraded.
	}

	private function columnExists($table, $column) {
		$query = $this->db->query("SHOW COLUMNS FROM `" . DB_PREFIX . $this->db->escape($table) . "` LIKE '" . $this->db->escape($column) . "'");

		return (bool)$query->num_rows;
	}
}
